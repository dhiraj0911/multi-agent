from typing import Literal
from pydantic import BaseModel, Field

class RouteDecision(BaseModel):
    next_agent: Literal["rag", "web_search", "execution", "synthesis", "end"] = Field(
        description="Which agent should act next, or 'end' if done"
    )
    is_completed: bool = Field(
        description="True if enough information has been gathered to answer the user"
    )
    reasoning: str = Field(
        description="Brief reasoning for this routing decision"
    )