from graphs.state_schema import WorkflowState

def checking_missing_info(state: WorkflowState) -> str:
    if state['missing_fields']:
        return 'ask_clarification'

    return 'generate_workflow'

def check_uncertainty(state: WorkflowState) -> str:
    if state['uncertainty_flag']:
        return 'ask_clarification'

    return 'extract_info'
