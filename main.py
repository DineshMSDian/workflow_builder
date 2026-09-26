from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from graphs.builder import build_graph
from graphs.state_schema import WorkflowState
from typing import cast
from dotenv import load_dotenv

from configs import MODEL

load_dotenv()

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
        if state["final_workflow"]:
            print("\nDone:", state["final_workflow"])
            break

        print(f"Bot: {state['messages'][-1].content}")
        user_input = input("You: ")

        # Subsequent calls: only pass the new message — checkpointer has the rest
        state = cast(WorkflowState, app.invoke(cast(WorkflowState, {"messages": [HumanMessage(content=user_input)]}), config))

if __name__ == "__main__":
    main()