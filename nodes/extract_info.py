from graphs.state_schema import WorkflowState

ALL_REQUIRED_FIELDS = [
    'trigger_source', 'trigger_event', 'condition', 'action', 'destination', 'notification_channel', 'duplicate_handling'
]

def extract_info(state: WorkflowState):
    available_info = state['extracted_info']
    missing_fields = []

    for field in ALL_REQUIRED_FIELDS:
        if available_info.get(field) is None:
            missing_fields.append(field)

    return {'missing_fields': missing_fields}




















if __name__ == '__main__':
    from nodes.understand_intent import understand_intent
    from configs import MODEL
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    load_dotenv()
    llm = ChatOpenAI(model=MODEL, temperature=0.2)
    test_state: WorkflowState = {
        'messages': [HumanMessage(content='notify me on telegram when a new file is added to my google drive')],
        'user_intent': '',
        'extracted_info': {},
        'missing_fields': [],
        'questions_asked': [],
        'current_question': '',
        'uncertainty_flag': False,
        'workflow_ready': False,
        'final_workflow': None
    }
    result = understand_intent(test_state, llm)
    test_state.update(result)           # merge intent + extracted_info back in
    missing_fields = extract_info(test_state)
    print(missing_fields)