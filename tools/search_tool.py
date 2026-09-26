from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

# TAVILY_API_KEY is read from the env
search_tool = TavilySearch(max_results=5)

tools = [search_tool]
_tool_node = ToolNode(tools)

def search_tool_node(state):
    result = _tool_node.invoke(state)
    tool_messages = result["messages"]
    return {
        "messages": tool_messages,
        "web_search_result": "\n".join(str(m.content) for m in tool_messages),
    }