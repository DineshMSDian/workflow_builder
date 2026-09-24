import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
import json

SYSTEM_PROMPT = """
You are a workflow builder assistant.

Your job:
1. Understand what the user wants to automate
2. Identify what information is missing
3. Ask ONE clarification question at a time
4. When you have enough info, output EXACTLY:
   WORKFLOW_READY
   {json here}

Rules:
- Never assume missing information
- Ask only one question per turn
- If the user's answer is ambiguous, ask for clarification
- Required fields: trigger_source, trigger_event, condition, 
  action, destination, additional_params

Understand the user's automation request.

For every turn:
    - identify information already provided
    - identify missing information
    - detect ambiguity
    - never assume missing information
    - ask ONE clarification question if information is insufficient
"""

load_dotenv()

converstaion_state: list[BaseMessage] = [
    SystemMessage(content=SYSTEM_PROMPT),
]

llm = ChatOpenAI(model='google/gemini-2.5-flash-lite', temperature=0.2)

while True:
    user_input = input('Enter Your Query: ')
    converstaion_state.append(HumanMessage(content=user_input))
    response = llm.invoke(input=converstaion_state)
    converstaion_state.append(AIMessage(content=response.content))

    if 'WORKFLOW_READY' in response.content:
        print(response.content)
        break
    else:
        print(response.content)