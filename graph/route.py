from graph.state import State

def route_from_coordinator(state: State):
    if state["is_completed"]:
        return "synthesis"
    return state["next_agent"]