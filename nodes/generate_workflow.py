from langchain_core.messages import AIMessage, SystemMessage
from graphs.state_schema import WorkflowState
import json

def generate_workflow(state: WorkflowState, llm) -> dict:
    prompt = f"""
Based on this collected info, generate a clean structured automation workflow JSON.

Intent: {state["user_intent"]}
Info: {state["extracted_info"]}

Output valid JSON only.
"""

    response = llm.invoke([SystemMessage(content=prompt)])
    workflow = json.loads(response.content)

    return {
        'final_workflow': workflow,
        'messages': [AIMessage(content=f'\nWorkflow Ready:\n{json.dumps(workflow, indent=2)}')]
    }