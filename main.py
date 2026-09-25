from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from graphs.builder import build_graph
from dotenv import load_dotenv

from configs import MODEL

load_dotenv()

def main():
    llm = ChatOpenAI(model=MODEL, temperature=0.2)
    app = build_graph(llm)

    state = {
        "messages": [],
        "intent": "",
        "extracted_info": {},
        "missing_fields": [],
        "questions_asked": [],
        "current_question": "",
        "uncertainty_flag": False,
        "final_workflow": None
    }
    
    # first message
    user_input = input("What do you want to automate? ")
    state["messages"] = [HumanMessage(content=user_input)]
    
    while True:
        state = app.invoke(state)
        
        if state["final_workflow"]:
            print("\nDone:", state["final_workflow"])
            break
        
        # get next user input after clarification question was asked
        user_input = input("You: ")
        state["messages"].append(HumanMessage(content=user_input))

if __name__ == "__main__":
    main()