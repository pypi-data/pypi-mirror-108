from dataclasses import dataclass
from typing import Literal, Optional, Tuple, List

import sqlite3;

from subsql.parser import parser, util, ParserSnippet, ParserError

@dataclass
class SQLiteCommand:
    name: str
    query: str
    returns: Literal["one", "many", "scalar", "void", "rowcount", "lastrowid"]
    execute: Optional[Literal["many", "script"]]
    modifier: Optional[str]

return_types = ["one", "many", "scalar", "void", "rowcount", "lastrowid"]
supported_options = ["name", "execute", "doc"] + return_types

def parse(path: str) -> Tuple[List[ParserError], List[SQLiteCommand]]:
    errors = [] # list of errors to display to user
    command_objects = [] # command objects

    snippets: List[ParserSnippet] = parser.parse_file(path)

    if not snippets:
        errors.append(ParserError(message="No SQL snippets found", file=path, lineno=1))

    seen = []

    for snippet in snippets:
        name_option = util.get_option(snippet, "name")

        if not name_option or not name_option.value:
            errors.append(ParserError(message="Snippet doesn't have a name", file=snippet.file, lineno=snippet.lineno))
            continue

        command_name = name_option.value

        if command_name in seen:
            errors.append(ParserError(
                message=f"Command {command_name} already exists",
                file=snippet.file,
                lineno=snippet.lineno
            ))
            continue
        else:
            seen.append(command_name)

        if unsupported_options := [s for s in snippet.options if s.name not in supported_options]:
            for unsupported in unsupported_options:
                errors.append(ParserError(
                    message=f"Unsupported option {unsupported.name}",
                    file=unsupported.file,
                    lineno=unsupported.lineno
                ))
            continue

        if duplicate_options := util.get_duplicate_options(snippet):
            errors.append(ParserError(
                message="Found duplicate option " + ', '.join(duplicate_options),
                file=snippet.file,
                lineno=snippet.lineno
            ))
            continue

        if not snippet.sql:
            errors.append(ParserError(message=f"No query found for command {command_name}", file=snippet.file, lineno=snippet.lineno))
            continue
        
        # since we don't allow duplicate option names let's convert options list to a dict
        options = util.get_options_dict(snippet.options)

        # we'll start collect arugments to SQLiteCommand here
        args = {"name": command_name, "query": snippet.sql}

        returns = [o for o in options if o in return_types]

        if len(returns) == 0:
            args["returns"] = "void"
        elif len(returns) == 1:
            args["returns"] = returns[0]
        else:
            errors.append(ParserError(
                message="Multiple returns types (" + ', '.join(returns) + f") specified for command {command_name}",
                file=snippet.file,
                lineno=snippet.lineno
            ))
            continue

        if "execute" in options:
            execute_option = options["execute"]
            execute_value = execute_option.value
            if execute_value in ["many", "script"]:
                args["execute"] = execute_value
            else:
                errors.append(ParserError(
                    message=f"Parameter to :execute must be 'many' or 'script', not '{execute_value}'",
                    file=execute_option.file,
                    lineno=execute_option.lineno
                ))
                continue
        else:
            args["execute"] = None

        args["modifier"] = None

        command_objects.append(SQLiteCommand(**args))

    return errors, command_objects

def execute(self, command, args=None, cursor=None, format=None, modifier=None):
    cursor = cursor if cursor else self.conn.cursor()
    query = format(command.query) if format else command.query
    modifier = modifier if modifier else command.modifier

    if command.execute == "many":
        cursor.executemany(query, args)
    elif command.execute == "script":
        cursor.executescript(query)
    else:
        if args is None:
            cursor.execute(query)
        else:
            cursor.execute(query, args)

    if command.returns == "one":
        result = cursor.fetchone()
        if modifier:
            if modifier in self.modifiers:
                return self.modifiers[modifier](result)
            else:
                raise f"Unknown modifier {command.modifier}"
        else:
            return result
    elif command.returns == "many":
        results = cursor.fetchall()
        if modifier:
            if modifier in self.modifiers:
                return [self.modifiers[modifier](r) for r in results]
            else:
                raise f"Unknown modifier {command.modifier}"
        else:
            return results
    elif command.returns == "scalar":
        result = cursor.fetchone()[0]
    elif command.returns == "void":
        result = None
    elif command.returns == "rowcount":
        result = cursor.rowcount
    elif command.returns == "lastrowid":
        result = cursor.lastrowid
    else:
        raise f"Unknown return type {command.returns}"

    return result

