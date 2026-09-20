from typing import Optional, TypedDict, Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str
    rag_result: str
    web_search_result: str
    execution_result: str
    synthesis_result: str
    final_result: str

    next_agent: Optional[str]
    is_completed: bool
