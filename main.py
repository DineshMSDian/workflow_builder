import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
import json

load_dotenv()

def build_system_prompt():
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

    return SYSTEM_PROMPT

def chat(user_input, messages, llm):

    messages.append(HumanMessage(user_input))
    response = llm.invoke(messages)
    messages.append(response.content)
    return response.content, messages

def is_workflow_ready(response) -> bool:
    return 'WORKFLOW_READY' in response

def extract_workflow(response):
    json_part = response.split('WORKFLOW_READY')[1].strip()
    json_part = json_part.replace('```json', '').replace('```', '').strip()
    return json.loads(json_part)

def main():
    conversation_state = [
        SystemMessage(content=build_system_prompt()),
    ]
    llm = ChatOpenAI(model='google/gemini-2.5-flash-lite', temperature=0.2)
    
    while True:
        user_input = input('Enter Your Query: ')
        response, conversation_state = chat(user_input, conversation_state, llm)
        if is_workflow_ready(response):
            workflow = extract_workflow(response)
            print(workflow)
            break
        else:
            print(response)

if __name__ == '__main__':
    main()