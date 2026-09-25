from typing import TypedDict, Annotated, Literal, List, Dict, Optional
from langgraph.graph import add_messages

class WorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    user_intent: str
    extracted_info: Dict
    missing_fields: List[str]
    questions_asked: List[str]
    current_question: str
    uncertainty_flag: bool
    workflow_ready: bool
    final_workflow: Optional[Dict]