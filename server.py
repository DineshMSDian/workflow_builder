import os
import sys
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import cast

from configs import MODEL
from graphs.builder import build_graph
from graphs.state_schema import WorkflowState

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI(
    title="Workflow Builder API",
    description="Conversational Automation Workflow Builder API powered by LangGraph",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ca-frontend.kindrock-91ecbb54.southindia.azurecontainerapps.io",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM & LangGraph Graph
llm = ChatOpenAI(model=MODEL, temperature=0.2)
graph_app = build_graph(llm)

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "default_session"

class ChatResponse(BaseModel):
    message: str
    status: str  # "needs_clarification" | "complete"
    workflow: Optional[Dict[str, Any]] = None
    extracted_info: Dict[str, Any] = {}
    missing_fields: list[str] = []
    thread_id: str

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model": MODEL}

@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    thread_id = request.thread_id or "default_session"
    config = {"configurable": {"thread_id": thread_id}}

    try:
        # Check current state from checkpointer
        current_state = graph_app.get_state(config)
        
        # If thread has no existing state, send full initial payload
        if not current_state or not current_state.values:
            input_payload = {
                "messages": [HumanMessage(content=request.message.strip())],
                "user_intent": "",
                "extracted_info": {},
                "missing_fields": [],
                "questions_asked": [],
                "current_question": "",
                "current_field": None,
                "uncertainty_flag": False,
                "uncertainty_reason": None,
                "final_workflow": None
            }
        else:
            # Subsequent turn: only pass the new message
            input_payload = {"messages": [HumanMessage(content=request.message.strip())]}

        state = cast(WorkflowState, graph_app.invoke(input_payload, config))

        # Check if workflow was generated
        if state.get("final_workflow"):
            bot_message = ""
            if state.get("messages"):
                last_msg = state["messages"][-1]
                bot_message = getattr(last_msg, "content", str(last_msg))
            if not bot_message:
                bot_message = "Workflow generated successfully!"

            return ChatResponse(
                message=bot_message if isinstance(bot_message, str) else str(bot_message),
                status="complete",
                workflow=state["final_workflow"],
                extracted_info=state.get("extracted_info", {}),
                missing_fields=[],
                thread_id=thread_id
            )
        else:
            # Still needs clarification
            bot_question = state.get("current_question")
            if not bot_question and state.get("messages"):
                last_msg = state["messages"][-1]
                bot_question = getattr(last_msg, "content", str(last_msg))

            return ChatResponse(
                message=bot_question or "Could you clarify the next detail?",
                status="needs_clarification",
                workflow=None,
                extracted_info=state.get("extracted_info", {}),
                missing_fields=state.get("missing_fields", []),
                thread_id=thread_id
            )

    except Exception as e:
        print(f"Error handling chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
def reset_session(request: ChatRequest):
    thread_id = request.thread_id or "default_session"
    # To reset in memory saver, invoke with empty state or new thread_id
    return {"status": "reset", "thread_id": thread_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
