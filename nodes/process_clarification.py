from langchain_core.messages import SystemMessage
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional

class ClarificationOutput(BaseModel):
    is_clear: bool
    field: Optional[str] = None
    value: Optional[str] = None
    uncertainty_reason: Optional[str] = None

ALL_REQUIRED_FIELDS = [
    'trigger_source', 'trigger_event', 'condition', 'action', 'destination',
    'notification_channel', 'duplicate_handling'
]

def normalize_field(field: str | None) -> str | None:
    if not field:
        return None
    if field in ALL_REQUIRED_FIELDS:
        return field
    # handle spaces/dashes the LLM might use
    cleaned = field.lower().strip().replace(' ', '_').replace('-', '_')
    return cleaned if cleaned in ALL_REQUIRED_FIELDS else None

def process_clarification_response(state: WorkflowState, llm) -> dict:
    user_message = []
    for message in state['messages']:
        if message.type == 'human':
            user_message.append(message)

    last_user_message = user_message[-1]

    prompt = f"""
The workflow being built: {state["user_intent"]}
The question that was asked: {state["current_question"]}
The user's answer: {last_user_message.content}

Tasks:
1. Is this answer clear and unambiguous? (yes/no)
2. If yes, which field does it fill and what is the exact value?
3. If no, briefly state why it is unclear.

Respond ONLY in this JSON:
{{
  "is_clear": true/false,
  "field": "field_name or null",
  "value": "extracted value or null",
  "uncertainty_reason": "why it is unclear, or null if clear"
}}
"""
    
    structured_llm = llm.with_structured_output(ClarificationOutput)
    result: ClarificationOutput = structured_llm.invoke([SystemMessage(content=prompt)])

    updated_info = state['extracted_info'].copy()
    if result.is_clear and result.field:
        canonical = normalize_field(result.field)
        if canonical:
            updated_info[canonical] = result.value

    return {
        'extracted_info': updated_info,
        'uncertainty_flag': not result.is_clear,
        'uncertainty_reason': result.uncertainty_reason if not result.is_clear else None
    }