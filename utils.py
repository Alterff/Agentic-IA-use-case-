from langchain_core.tools import tool
@tool
def multiply_by_two(arg: int) -> int:
    """Multiply a number by two."""
    return arg * 2

@tool
def add_five(arg: int) -> int:
    """Add value to a number."""
    return arg + 5

TOOLS = {
    "multiply_by_two": multiply_by_two,
    "add_five": add_five,
}



