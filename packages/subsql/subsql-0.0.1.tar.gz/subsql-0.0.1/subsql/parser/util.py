from typing import Dict, List, Optional;
from .types import ParserSnippet, ParserOption

def get_unsupported_options(snippet: ParserSnippet, supported: List[str]) -> List[str]:
    """Get options whose names are not in the supported list"""
    return [s.name for s in snippet.options if s.name not in supported]

def get_duplicate_options(snippet: ParserSnippet):
    """Get options whose names are found more than once"""
    seen = []
    duplicates = []

    for option in snippet.options:
        if option.name in seen:
            duplicates.append(option.name)

        seen.append(option.name)

    return duplicates

def get_options_dict(options: List[ParserOption]) -> Dict[str, ParserOption]:
    """Get options as a dictionary keyed by option name"""
    options_dict = {}

    for option in options:
        options_dict[option.name] = option

    return options_dict

def get_option(snippet: ParserSnippet, name: str) -> Optional[ParserOption]:
    """Get first option with the given name"""
    for option in snippet.options:
        if option.name == name:
            return option

