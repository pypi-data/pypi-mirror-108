"""Class for parsing and formatting terminal messages"""

color_map = {
    "&r": "\033[1;31m",
    "&g": "\033[1;32m",
    "&y": "\033[1;33m",
    "&b": "\033[1;34m",
    "&m": "\033[1;35m",
    "&c": "\033[1;36m",
    "&&": "\033[0m"
}


def colparse(instr: str) -> str:
    for col, fmt in color_map.items():
        instr.replace(col, fmt)
    return instr
