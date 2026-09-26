from langgraph.graph import StateGraph, START, END

from graph.state import State
from graph.route import route_from_coordinator, route_after_execution, route_after_web_search

from agents.coordinator import coordinator_agent_node
from agents.execution_agent import execution_agent_node
from agents.synthesis_agent import synthesis_agent_node
from agents.web_search_agent import web_search_agent_node

from tools.complex_calculation import execution_tool_node
from tools.search_tool import search_tool_node

graph = StateGraph(State)

# add nodes
graph.add_node("coordinator", coordinator_agent_node)
graph.add_node("execution_agent", execution_agent_node)
graph.add_node("web_search_agent", web_search_agent_node)
graph.add_node("execution_tools", execution_tool_node)
graph.add_node("web_search_tools", search_tool_node)
graph.add_node("synthesis", synthesis_agent_node)

# add edges
graph.add_edge(START, "coordinator")

# --------------------
# Coordinator routing
# --------------------
graph.add_conditional_edges(
    "coordinator",
    route_from_coordinator,
    {
        "synthesis": "synthesis",
        "execution": "execution_agent",
        "web_search": "web_search_agent",
    }
)

# Execution agent routing
graph.add_conditional_edges(
    "execution_agent",
    route_after_execution,
    {
        "execution_tools": "execution_tools",
        "coordinator": "coordinator",
    }
)
graph.add_edge(
    "execution_tools",
    "coordinator"
)

# Web Search Agent routing
graph.add_conditional_edges(
    "web_search_agent",
    route_after_web_search,
    {
        "web_search_tools": "web_search_tools",
        "coordinator": "coordinator",
    }
)
graph.add_edge(
    "web_search_tools",
    "coordinator"
)

graph.add_edge("synthesis", END)

app = graph.compile()