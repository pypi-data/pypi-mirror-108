import re
from typing import List, Literal;
from .types import ParserLine, ParserOption, ParserSnippet, ParserError

###########
# METHODS #
###########

def parse_file(path: str) -> List[ParserSnippet]:
    """Main entry point, takes a file name and produces a list of snippets"""
    lines: List[ParserLine] = read_lines(path)
    groups_of_lines: List[List[ParserLine]] = group_lines(lines)
    snippets: List[ParserSnippet] = [process_group(g) for g in groups_of_lines]

    return snippets

def read_lines(path: str) -> List[ParserLine]:
    """Splits a file into lines, marking each as either comment or sql"""

    with open(path, 'r') as reader:
        lines: List[ParserLine] = []

        current: str = reader.readline()
        lineno = 1

        while current != '':  # The EOF char is an empty string
            type = "comment" if re.search('--\s*:', current) else "sql";
            lines.append(ParserLine(type=type, text=current, lineno=lineno, file=path))
            
            current = reader.readline()
            lineno = lineno + 1

    return lines

def group_lines(lines: List[ParserLine]) -> List[List[ParserLine]]:
    """Identifies and groups together lines belonging to the same snippet"""

    context: Literal["start", "comment", "sql"] = 'start'
    current_group: List[ParserLine] = []
    all_groups: List[List[ParserLine]] = []

    for line in lines:
        # skip initial lines until we find the first matching comment
        if line.type != "comment" and not current_group:
            continue

        # this is the start of a new snippet, setup new current_group
        if line.type == "comment" and context != "comment":
            if current_group: all_groups.append(current_group)
            current_group = []

        current_group.append(line)
        context = "comment" if line.type == "comment" else "sql"

    # don't forget the last group, the loop won't catch it
    all_groups.append(current_group)

    return all_groups

def process_group(group: List[ParserLine]) -> ParserSnippet:
    """Converts a group of lines into a snippet object"""
    options: List[ParserOption] = []

    if len(group):
        file = group[0].file
        lineno = group[0].lineno

    for line in group:
        if line.type == "comment":
            options.extend(parse_options(line))

    sql: str = "".join([l.text for l in group if l.type == "sql"]).strip()

    return ParserSnippet(options=options, sql=sql, file=file, lineno=lineno)    

def parse_options(line: ParserLine) -> List[ParserOption]:
    """Parses a comment line into a list of options"""
    code: str = re.sub('^-*', '', line.text).strip()
    options: List[ParserOption] = []
    command_re = r'(\:\w+)'
    parts: List[str] = re.split(command_re, code)

    for part in parts:
        if part == '':
            continue
        elif re.match(command_re, part):
            options.append(ParserOption(
                name=part.lstrip(":"),
                value=None,
                modifier=None,
                file=line.file,
                lineno=line.lineno
            ))
        elif match := re.match(r'\s*(\w+)\((\w+)\)\s*$', part):
            options[-1].value = match.group(1)
            options[-1].modifier = match.group(2)
        else:
            options[-1].value = part.strip()

    return options

