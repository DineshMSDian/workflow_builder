from langchain_core.messages import SystemMessage, AIMessage


#System Prompt
QUESTION_PROMPT = """You are a friendly assistant helping a user set up an automation workflow.

Workflow goal: {user_intent}
Information collected so far: {extracted_info}

{context}

Your task: Generate ONE short, friendly question asking the user for the value of "{field_name}".
- Include an example or hint if helpful (e.g., "Which Gmail label? For example, 'Finance' or 'Invoices'")
- Be conversational and natural
- Keep it to 1-2 sentences

Respond with ONLY the question text. No prefixes, no numbering, just the question.
"""


def ask_clarification(state: dict, llm) -> dict:
    """
    Generate one clarification question for the next missing field.

    Flow:
      If uncertainty_flag → re-ask the SAME field with clarification context
      Else → pick the FIRST missing field and ask about it

      Python picks the field → LLM writes the question → return both

    Example:
      missing_fields = ["filter_condition", "recipient"]
      → target_field = "filter_condition"
      → LLM generates: "What filtering rules should I apply? For example, 'amount > 10000'"
      → returns { current_field: "filter_condition", current_question: "What filtering..." }

    Returns:
      dict to merge into state:
        {
          "current_field": "filter_condition",
          "current_question": "What filtering rules should I apply?",
          "questions_asked": [..., "What filtering rules..."],
          "uncertainty_flag": False,
          "uncertainty_reason": None,
        }
    """
    missing = state.get("missing_fields", [])
    already_asked = state.get("questions_asked", [])

    if state.get("uncertainty_flag") and state.get("current_field"):
        # Re-ask the same field — the previous answer was unclear
        target_field = state["current_field"]
        context = (
            f"The user's previous answer was unclear. "
            f"Reason: {state.get('uncertainty_reason', 'ambiguous response')}. "
            f"Politely ask them to clarify their answer for '{target_field}'."
        )
    else:
        # Pick the first missing field
        target_field = missing[0] if missing else "additional_preferences"
        context = f"This is a fresh question — ask about '{target_field}' for the first time."

    prompt = QUESTION_PROMPT.format(
        user_intent=state.get("user_intent", "automation workflow"),
        extracted_info=state.get("extracted_info", {}),
        field_name=target_field,
        context=context,
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
