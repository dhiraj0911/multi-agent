from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def get_square(input_data: str):
    """Compute the square of the input data."""
    result = int(input_data) ** 2  # Example computation
    print(f"Computed square of {input_data}: {result}")
    return result

@tool
def get_cube(input_data: str):
    """Compute the cube of the input data."""
    result = int(input_data) ** 3  # Example computation
    return result

@tool
def get_quartic(input_data: str):
    """Compute the quartic (fourth power) of the input data."""
    result = int(input_data) ** 4  # Example computation
    return result

tools = [
    get_square, 
    get_cube, 
    get_quartic
]

_tool_node = ToolNode(tools)

def execution_tool_node(state):
    result = _tool_node.invoke(state)
    tool_messages = result["messages"]
    return {
        "messages": tool_messages,
        "execution_result": "\n".join(str(m.content) for m in tool_messages),
    }