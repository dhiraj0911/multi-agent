from langgraph.graph import StateGraph, START, END

from graph.state import State
from graph.route import route_from_coordinator

from agents.coordinator import coordinator_agent_node
from agents.execution_agent import execution_agent_node
from agents.synthesis_agent import synthesis_agent_node
from agents.web_search_agent import web_search_agent_node

graph = StateGraph(State)

# add nodes
graph.add_node("coordinator", coordinator_agent_node)
graph.add_node("execution", execution_agent_node)
graph.add_node("synthesis", synthesis_agent_node)
graph.add_node("web_search", web_search_agent_node)

# add edges
graph.add_edge(START, "coordinator")
graph.add_conditional_edges(
    "coordinator",
    route_from_coordinator,
    {
        "synthesis": "synthesis",
        "execution": "execution",
        "web_search": "web_search"
    }
)

# after each sub-agent route back to coordinator agent
graph.add_edge("execution", "coordinator")
graph.add_edge("web_search", "coordinator")

graph.add_edge("synthesis", END)

app = graph.compile()