from langchain_core.messages import AIMessage
from graphs.state_schema import WorkflowState
import json

def generate_workflow(state: WorkflowState, llm) -> dict:
    extracted = state.get("extracted_info", {})
    
    trigger_source = extracted.get("trigger_source") or "Trigger Service"
    trigger_event = extracted.get("trigger_event") or "New Event"
    condition = extracted.get("condition")
    action = extracted.get("action") or "Process Data"
    destination = extracted.get("destination") or "Storage"
    notification_channel = extracted.get("notification_channel") or "Notification"
    duplicate_handling = extracted.get("duplicate_handling")

    nodes = []
    edges = []

    # 1. Trigger Node
    nodes.append({
        "id": "trigger",
        "type": "trigger",
        "label": f"{trigger_source} Trigger",
        "description": trigger_event
    })

    # 2. Action / Processing Node
    nodes.append({
        "id": "action",
        "type": "action",
        "label": action.title() if isinstance(action, str) else "Process Request",
        "description": f"Target: {destination}" if destination else "Execute Action"
    })
    edges.append({
        "source": "trigger",
        "target": "action"
    })

    prev_node_id = "action"

    # 3. Condition Node (if condition specified and not "none")
    has_condition = condition and str(condition).lower() not in ["none", "no", "no condition", "false"]

    if has_condition:
        nodes.append({
            "id": "condition",
            "type": "condition",
            "label": "Condition",
            "description": condition
        })
        edges.append({
            "source": prev_node_id,
            "target": "condition"
        })

        # Branch 1 (Yes): Notification
        nodes.append({
            "id": "notification",
            "type": "notification",
            "label": f"{notification_channel}",
            "description": "Send alert"
        })
        edges.append({
            "source": "condition",
            "target": "notification",
            "label": "Yes"
        })

        # Branch 2 (No): End
        nodes.append({
            "id": "end_no",
            "type": "end",
            "label": "End",
            "description": "Skip process"
        })
        edges.append({
            "source": "condition",
            "target": "end_no",
            "label": "No"
        })

        # Connect Notification -> End
        nodes.append({
            "id": "end_yes",
            "type": "end",
            "label": "End",
            "description": "Completed"
        })
        edges.append({
            "source": "notification",
            "target": "end_yes"
        })

    else:
        # Sequential path without condition
        nodes.append({
            "id": "notification",
            "type": "notification",
            "label": f"{notification_channel}",
            "description": "Send Alert / Log"
        })
        edges.append({
            "source": prev_node_id,
            "target": "notification"
        })

        nodes.append({
            "id": "end",
            "type": "end",
            "label": "End",
            "description": "Completed"
        })
        edges.append({
            "source": "notification",
            "target": "end"
        })

    workflow_json = {
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "trigger_source": trigger_source,
            "trigger_event": trigger_event,
            "condition": condition,
            "action": action,
            "destination": destination,
            "notification_channel": notification_channel,
            "duplicate_handling": duplicate_handling
        }
    }

    return {
        'final_workflow': workflow_json,
        'messages': [AIMessage(content=f"Workflow generation complete! Created {len(nodes)} visual steps.")]
    }