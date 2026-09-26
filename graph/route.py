from graph.state import State

def route_from_coordinator(state: State):
    if state["is_completed"]:
        return "synthesis"
    return state["next_agent"]

def route_after_execution(state: State):
    message = state["messages"][-1]
    if message.tool_calls:
        return "execution_tools"
    return "coordinator"

def route_after_web_search(state: State):
    message = state["messages"][-1]
    if message.tool_calls:
        return "web_search_tools"
    return "coordinator"