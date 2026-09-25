from langchain_core.messages import SystemMessage
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional

class ClarificationOutput(BaseModel):
    is_clear: bool
    field: Optional[str] = None
    value: Optional[str] = None

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
2. If yes, which field does it fill and what is the value?

Respond ONLY in this JSON:
{{
  "is_clear": true/false,
  "field": "field_name or null",
  "value": "extracted value or null"
}}
"""
    
    structured_llm = llm.with_structured_output(ClarificationOutput)
    result: ClarificationOutput = structured_llm.invoke([SystemMessage(content=prompt)])

    updated_info = state['extracted_info'].copy()
    if result.is_clear and result.field:
        updated_info[result.field] = result.value

    return {
        'extracted_info': updated_info,
        'uncertainty_flag': not result.is_clear
    }