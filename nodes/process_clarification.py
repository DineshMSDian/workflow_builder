from langchain_core.messages import SystemMessage
from graphs.state_schema import WorkflowState
from pydantic import BaseModel
from typing import Optional

# Fields where a specific value is REQUIRED — bare yes/no/nothing is never valid
SPECIFIC_VALUE_FIELDS = {'trigger_source', 'trigger_event', 'action', 'destination', 'notification_channel'}

# Words that are never a real answer for specific-value fields
BARE_NONANSWERS = {
    'yes', 'no', 'ok', 'sure', 'yeah', 'yep', 'nope', 'nah', 'yea', 'ya',
    'idk', 'maybe', 'nothing', 'dunno', 'whatever', 'i dont know',
}

YES_VALUES = {
    'yes', 'yeah', 'yep', 'yea', 'ya', 'sure'
}

NO_VALUES = {
    'no', 'nope', 'nah'
}

# Words and physical objects that are never valid digital software apps or channels
PHYSICAL_NON_DIGITAL = {
    'pocket', 'my pocket', 'in my pocket', 'hair', 'air', 'hand', 'head', 'mind', 'bag', 'wallet',
    'desk', 'car', 'house', 'room', 'table', 'chair', 'paper', 'notebook', 'pen',
    'mouth', 'eye', 'eyes', 'ear', 'ears', 'foot', 'feet', 'leg', 'legs'
}

# What each field expects — gives the LLM a concrete reference for validation
FIELD_EXPECTATIONS = {
    'trigger_source': 'a real digital app or service (e.g. Gmail, Shopify, Slack, Google Drive, Bank API, Splitwise)',
    'trigger_event': 'a specific digital/software event (e.g. "new email received", "file uploaded", "new transaction")',
    'condition': 'a filter/rule (e.g. "amount > 1000", "only raids") OR "none" if no conditions',
    'action': 'what the system should DO (e.g. "send a message", "update a spreadsheet row", "track expenses")',
    'destination': 'a real app or storage service (e.g. Google Sheets, Notion, Excel, database)',
    'notification_channel': 'a real messaging service (e.g. Telegram, Slack, email, WhatsApp, SMS)',
    'duplicate_handling': '"yes" to skip duplicates or "no" to allow them',
}

class ClarificationOutput(BaseModel):
    is_clear: bool
    value: Optional[str] = None
    uncertainty_reason: Optional[str] = None

def process_clarification_response(state: WorkflowState, llm) -> dict:
    user_messages = [m for m in state['messages'] if m.type == 'human']
    last_user_message = user_messages[-1]
    answer_text = last_user_message.content.strip()
    current_field = state.get('current_field')

    answer_lower = answer_text.lower().strip().rstrip('.!?')

    if current_field == "duplicate_handling":

        if answer_lower in YES_VALUES:
            updated_info = state['extracted_info'].copy()
            updated_info[current_field] = "yes"

            return {
                'extracted_info': updated_info,
                'uncertainty_flag': False,
                'uncertainty_reason': None
            }

        if answer_lower in NO_VALUES:
            updated_info = state['extracted_info'].copy()
            updated_info[current_field] = "no"

            return {
                'extracted_info': updated_info,
                'uncertainty_flag': False,
                'uncertainty_reason': None
            }

        return {
            'extracted_info': state['extracted_info'].copy(),
            'uncertainty_flag': True,
            'uncertainty_reason':
                'Please answer yes or no about skipping duplicate events.'
        }

    if current_field == "condition":

        if answer_lower in {
            "none",
            "no",
            "no condition",
            "no conditions",
            "no filter",
            "no filters"
        }:
            updated_info = state['extracted_info'].copy()
            updated_info[current_field] = "none"

            return {
                'extracted_info': updated_info,
                'uncertainty_flag': False,
                'uncertainty_reason': None
            }

    if current_field in SPECIFIC_VALUE_FIELDS:

        if answer_lower in BARE_NONANSWERS:
            expected = FIELD_EXPECTATIONS.get(
                current_field,
                'a specific value'
            )

            return {
                'extracted_info': state['extracted_info'].copy(),
                'uncertainty_flag': True,
                'uncertainty_reason':
                    f'"{answer_text}" is not a specific value. '
                    f'I need {expected}.'
            }


    field_hint = (
        FIELD_EXPECTATIONS.get(current_field, 'a specific, concrete value')
        if current_field is not None
        else 'a specific, concrete value'
    )
    prompt = f"""
You are validating ONE answer to a workflow clarification question.

Workflow goal:
{state["user_intent"]}

Question asked:
{state["current_question"]}

Required field:
{current_field}

Expected value:
{field_hint}

User's answer:
{answer_text}

Your job is NOT to guess what the user meant.

STRICT RULES:

1. Accept the answer ONLY if it directly answers the question.
2. Do not infer missing information.
3. Do not transform vague statements into concrete values.
4. If multiple interpretations are possible, mark unclear.
5. If the answer is unrelated, mark unclear.
6. If the answer is contradictory, mark unclear.
7. Minor spelling mistakes are acceptable.
8. Return the user's actual intended value only when it is clearly supported.
9. Never invent an app, service, event, action, destination, or channel.

Examples:

Question: "Which app or service should trigger the workflow?"
Answer: "my pocket"
→ unclear

Question: "Which app or service should trigger the workflow?"
Answer: "Google Sheets"
→ clear

Question: "What event should trigger the workflow?"
Answer: "yes"
→ unclear

Question: "What event should trigger the workflow?"
Answer: "when a new row is added"
→ clear

Question: "Are there any conditions?"
Answer: "no"
→ clear, value = "none"

Question: "Should duplicate events be skipped?"
Answer: "yes"
→ clear, value = "yes"

Question: "Should duplicate events be skipped?"
Answer: "of course not yes"
→ unclear

If unclear:
- is_clear = false
- value = null
- explain what information is missing.

If clear:
- is_clear = true
- value = the concrete value from the user's answer.

Return ONLY the structured output.
"""

    structured_llm = llm.with_structured_output(ClarificationOutput)
    result: ClarificationOutput = structured_llm.invoke([SystemMessage(content=prompt)])

    updated_info = state['extracted_info'].copy()
    if result.is_clear and result.value and current_field:
        updated_info[current_field] = result.value

    return {
        'extracted_info': updated_info,
        'uncertainty_flag': not result.is_clear,
        'uncertainty_reason': result.uncertainty_reason if not result.is_clear else None
    }