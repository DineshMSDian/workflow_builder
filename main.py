from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from graphs.builder import build_graph
from graphs.state_schema import WorkflowState
from typing import cast
from dotenv import load_dotenv
import json

from configs import MODEL

load_dotenv()

import sys
sys.stdout.reconfigure(encoding='utf-8')

FIELD_LABELS = {
    'trigger_source': 'Trigger Source',
    'trigger_event': 'Trigger Event',
    'condition': 'Condition',
    'action': 'Action',
    'destination': 'Destination',
    'notification_channel': 'Notification Channel',
    'duplicate_handling': 'Duplicate Handling',
}

def print_state_table(state):
    extracted = state.get('extracted_info', {})
    missing = state.get('missing_fields', [])
    print("\n  --- Collected Information ---")
    for field, label in FIELD_LABELS.items():
        value = extracted.get(field)
        marker = '[x]' if value else '[ ]'
        print(f"  {marker} {label}: {value or '-'}")
    filled = sum(1 for v in extracted.values() if v is not None)
    total = len(FIELD_LABELS)
    status = f"  Status: {filled}/{total} fields collected"
    if not missing:
        status += " -- Ready to generate!"
    print(status + "\n")

def main():
    llm = ChatOpenAI(model=MODEL, temperature=0.2)
    app = build_graph(llm)
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    user_input = input("What do you want to automate? ")

    # First call: pass full initial state once
    state: WorkflowState = cast(WorkflowState, app.invoke({
        "messages": [HumanMessage(content=user_input)],
        "user_intent": "",
        "extracted_info": {},
        "missing_fields": [],
        "questions_asked": [],
        "current_question": "",
        "current_field": None,
        "uncertainty_flag": False,
        "uncertainty_reason": None,
        "final_workflow": None
    }, config))

    while True:
        print_state_table(state)

        if state["final_workflow"]:
            print("[OK] Workflow Generated!")
            print(json.dumps(state["final_workflow"], indent=2))
            break

        print(f"Bot: {state['messages'][-1].content}")
        user_input = input("You: ")

        # Subsequent calls: only pass the new message — checkpointer has the rest
        state = cast(WorkflowState, app.invoke(cast(WorkflowState, {"messages": [HumanMessage(content=user_input)]}), config))

if __name__ == "__main__":
    main()