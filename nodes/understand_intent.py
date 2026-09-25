from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional

INTENT_PROMPT = """
You are an automation assistent. The user wants to build a workflow.
from their message, extract:
    - what they want to automate (intent)
    - Any info they already mentioned (trigger, action, destination, etc.)

RESPOND ONLY in this JSON format:
{
    'user_intent': "...",
    'extracted_info': {
        'trigger_source': null,
        'trigger_event': null,
        'condition': null,
        'action': null,
        'destination': null,
        'notification_channel': null,
        duplicate_handling': null,
    }
}
"""

class ExtractedInfo(BaseModel):
    trigger_source: Optional[str] = None
    trigger_event: Optional[str] = None
    condition: Optional[str] = None
    action: Optional[str] = None
    destination: Optional[str] = None
    notification_channel: Optional[str] = None
    duplicate_handling: Optional[str] = None

class IntentOutput(BaseModel):
    user_intent: str
    extracted_info: ExtractedInfo

def understand_intent(state: WorkflowState, llm) -> dict:
    structured_llm = llm.with_structured_output(IntentOutput)

    result: IntentOutput = structured_llm.invoke([
        SystemMessage(content=INTENT_PROMPT),
        state['messages'][-1]
    ])

    return {
        'user_intent': result.user_intent,
        'extracted_info': result.extracted_info.model_dump()
    }











if __name__ == '__main__':

    from configs import MODEL
    from dotenv import load_dotenv

    load_dotenv()

    llm = ChatOpenAI(model=MODEL, temperature=0.2)
    test_state: WorkflowState = {
        'messages': [HumanMessage(content='notify me on telegram when a new file is added to my google drive')],
        'user_intent': '',
        'extracted_info': {},
        'missing_fields': [],
        'questions_asked': [],
        'current_question': '',
        'uncertainty_flag': False,
        'workflow_ready': False,
        'final_workflow': None
    }
    result = understand_intent(test_state, llm)
    test_state.update(result)