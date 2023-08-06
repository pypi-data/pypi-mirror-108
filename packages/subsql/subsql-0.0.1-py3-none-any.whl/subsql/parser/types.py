from dataclasses import dataclass
from typing import Dict, List, Literal, Optional;

#########
# TYPES #
#########

@dataclass
class ParserLine:
    type: Literal["comment", "sql"]
    text: str
    file: str
    lineno: int

@dataclass
class ParserOption:
    name: str
    file: str
    lineno: int
    value: Optional[str]
    modifier: Optional[str]

@dataclass
class ParserSnippet:
    options: List[ParserOption]
    sql: str
    file: str
    lineno: int

@dataclass
class ParserError:
    message: str
    file: str
    lineno: int

    def __str__(self):
        return f"{self.message} at {self.file} line {self.lineno}"


