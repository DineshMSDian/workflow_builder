from langchain_core.messages import SystemMessage, AIMessage
from graphs.state_schema import WorkflowState

def ask_clarification(state: WorkflowState, llm) -> dict:
    missing = state['missing_fields']
    already_asked = state.get('questions_asked', [])

    prompt = f"""
You are collecting info to build an automation workflow.

Intent: {state["user_intent"]}
Already collected: {state["extracted_info"]}
Still missing: {missing}
Questions already asked: {already_asked}

Pick ONE missing field and ask a short, clear question about it.
Never repeat a question already asked.
Respond with ONLY the question, nothing else.
"""

    response = llm.invoke([SystemMessage(content=prompt)])
    question = response.content.strip()

    return {
        'current_question': question,
        'questions_asked': already_asked + [question],
        'messages': [AIMessage(content=question)]
    }