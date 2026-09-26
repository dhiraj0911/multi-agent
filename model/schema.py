from typing import Literal
from pydantic import BaseModel, Field

class RouteDecision(BaseModel):
    next_agent: Literal["rag", "web_search", "execution", "synthesis", "end"] = Field(
        description="Which agent should act next, or 'end' if done"
    )
    is_completed: bool = Field(
        description="true if the routing decision indicates that the process is completed"
    )
    reasoning: str = Field(
        description="Brief reasoning for this routing decision"
    )