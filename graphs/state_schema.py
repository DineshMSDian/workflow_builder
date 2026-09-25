from typing import TypedDict, Annotated, Literal, List, Dict, Optional
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class WorkflowState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_intent: str | None
    extracted_info: Dict
    missing_fields: List[str]
    questions_asked: List[str]
    current_question: str
    uncertainty_flag: bool
    workflow_ready: bool
    final_workflow: Optional[Dict]