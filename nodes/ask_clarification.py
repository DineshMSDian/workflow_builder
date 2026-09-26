from langchain_core.messages import SystemMessage, AIMessage


FIELD_DESCRIPTIONS = {
    'trigger_source': 'the app or service that sends the trigger (e.g. Gmail, Slack, Clash of Clans)',
    'trigger_event': 'the specific event that fires the workflow (e.g. new notification, file uploaded, form submitted)',
    'condition': 'any filter or rule on when to run (e.g. only raids, except promotional, amount above 1000)',
    'action': 'what the workflow should do when triggered (e.g. log the event, send a message, update a row)',
    'destination': 'where data should be stored (e.g. Google Sheets, Notion, a database)',
    'notification_channel': 'how the user should be alerted (e.g. Telegram bot, Slack message, email)',
    'duplicate_handling': 'whether duplicate events should be skipped (yes or no)',
}

QUESTION_PROMPT = """You are a friendly assistant helping a user set up an automation workflow.

Workflow goal: {user_intent}

Information already collected:
{collected_info}

{context}

Field still needed: "{field_name}"
What this field means: {field_description}

Ask ONE short, clear question to get this field's value.
Rules:
- Use what's already collected to frame a specific, relevant question
- Do NOT ask about anything already collected above
- Do NOT reference services/apps the user hasn't mentioned
- Keep it to 1-2 sentences, be direct
- Do NOT start with "Great!" or filler words

Respond with ONLY the question text.
"""

def ask_clarification(state: dict, llm) -> dict:
    missing = state.get("missing_fields", [])
    already_asked = state.get("questions_asked", [])
    extracted = state.get("extracted_info", {})

    # Build context of what's already been collected
    collected_lines = []
    for field, value in extracted.items():
        if value is not None:
            collected_lines.append(f"  - {field}: {value}")
    collected_info = "\n".join(collected_lines) if collected_lines else "  (none yet)"

    if state.get("uncertainty_flag") and state.get("current_field"):
        target_field = state["current_field"]
        context = (
            f"The user's previous answer was unclear. "
            f"Reason: {state.get('uncertainty_reason', 'ambiguous response')}. "
            f"Politely re-ask for '{target_field}', keeping it simple."
        )
    else:
        target_field = missing[0] if missing else "additional_preferences"
        context = f"Ask about '{target_field}'."

    prompt = QUESTION_PROMPT.format(
        user_intent=state.get("user_intent", "automation workflow"),
        field_name=target_field,
        field_description=FIELD_DESCRIPTIONS.get(target_field, target_field),
        context=context,
        collected_info=collected_info,
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    question_text = response.content.strip()

    return {
        "current_field": target_field,
        "current_question": question_text,
        "questions_asked": already_asked + [question_text],
        "uncertainty_flag": False,
        "uncertainty_reason": None,
        "messages": [AIMessage(content=question_text)],
    }