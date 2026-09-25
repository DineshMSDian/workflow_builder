from langchain_core.messages import AIMessage, SystemMessage
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional
import json

class WorkflowOutput(BaseModel):
    trigger_source: str
    trigger_event: str
    condition: Optional[str] = None
    action: str
    destination: str
    notification_channel: Optional[str] = None
    duplicate_handling: Optional[str] = None

def generate_workflow(state: WorkflowState, llm) -> dict:
    prompt = f"""
Based on this collected info, generate a clean structured automation workflow JSON.

Intent: {state["user_intent"]}
Info: {state["extracted_info"]}

Output valid JSON only.
"""
    structured_llm = llm.with_structured_output(WorkflowOutput)
    result: WorkflowOutput = structured_llm.invoke([SystemMessage(content=prompt)])
    workflow = result.model_dump()

    return {
        'final_workflow': workflow,
        'messages': [AIMessage(content=f'\nWorkflow Ready:\n{json.dumps(workflow, indent=2)}')]
    }