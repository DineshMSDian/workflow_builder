from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional

INTENT_PROMPT = """
You are an automation workflow requirement extractor.

Your job is to understand the user's request and extract ONLY information
that the user explicitly provided.

IMPORTANT RULES:

1. NEVER guess or assume missing information.
2. NEVER infer a value just because it seems likely.
3. If information is vague, ambiguous, contradictory, or incomplete, return null.
4. A yes/no answer is NOT valid for fields that require a specific value.
5. "none" is valid for condition ONLY when the user explicitly says there is
   no condition or filter.
6. Extract only what is supported by the user's actual message.
7. Preserve the user's meaning, but do not invent details.

Field definitions:

- trigger_source:
  The app/service/platform that produces the trigger.
  Example: Gmail, Slack, Clash of Clans.

- trigger_event:
  The specific event that starts the workflow.
  Example: new email received, file uploaded.

- condition:
  A rule/filter that controls when the workflow runs.
  Example: amount > 1000, only raids.
  "none" only when explicitly stated.

- action:
  What the workflow should do after the trigger.
  Example: send a message, log an event, update a row.

- destination:
  Where information should be stored or sent.
  Example: Google Sheets, Notion, database.

- notification_channel:
  How the user should be notified.
  Example: Telegram, Slack, email.

- duplicate_handling:
  Whether duplicate events should be skipped.
  Only extract this when the user explicitly specifies yes/no
  or an equivalent clear statement.

Return the information using the provided structured output schema.
Do NOT manually format the response as JSON.
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
        *state['messages']
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
        'current_field': '',
        'uncertainty_flag': False,
        'uncertainty_reason': '',
        'final_workflow': None,
    }
    result = understand_intent(test_state, llm)
    test_state.update(result)