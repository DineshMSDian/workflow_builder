from langchain_core.messages import AIMessage
from graphs.state_schema import WorkflowState
import json


def generate_workflow(state: WorkflowState, llm) -> dict:
    """Deterministically transforms collected explicit info into
    semantic node/edge JSON. The `service` field on each node
    tells the frontend which brand icon to render dynamically."""

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

    # ── 1. Trigger ──
    nodes.append({
        "id": "trigger",
        "type": "trigger",
        "label": f"{trigger_source} Trigger",
        "description": trigger_event,
        "service": trigger_source,
    })

    # ── 2. Action / Processing ──
    nodes.append({
        "id": "action",
        "type": "action",
        "label": action.title() if isinstance(action, str) else "Process",
        "description": f"Target: {destination}" if destination else "Execute",
        "service": destination,
    })
    edges.append({"source": "trigger", "target": "action"})

    prev_node_id = "action"

    # ── 3. Condition (optional) ──
    has_condition = (
        condition
        and str(condition).lower()
        not in ["none", "no", "no condition", "no conditions", "false"]
    )

    if has_condition:
        nodes.append({
            "id": "condition",
            "type": "condition",
            "label": "Condition",
            "description": condition,
            "service": "condition",
        })
        edges.append({"source": prev_node_id, "target": "condition"})

        # Yes branch → Notification
        nodes.append({
            "id": "notification",
            "type": "notification",
            "label": f"{notification_channel} Notification",
            "description": "Send alert",
            "service": notification_channel,
        })
        edges.append({
            "source": "condition",
            "target": "notification",
            "label": "Yes",
        })

        # No branch → End
        nodes.append({
            "id": "end_no",
            "type": "end",
            "label": "End",
            "description": "Condition not met",
            "service": "end",
        })
        edges.append({
            "source": "condition",
            "target": "end_no",
            "label": "No",
        })

        # Notification → End
        nodes.append({
            "id": "end_yes",
            "type": "end",
            "label": "End",
            "description": "Completed",
            "service": "end",
        })
        edges.append({"source": "notification", "target": "end_yes"})

    else:
        # ── Sequential (no condition) ──
        nodes.append({
            "id": "notification",
            "type": "notification",
            "label": f"{notification_channel} Notification",
            "description": "Send alert / log",
            "service": notification_channel,
        })
        edges.append({"source": prev_node_id, "target": "notification"})

        nodes.append({
            "id": "end",
            "type": "end",
            "label": "End",
            "description": "Completed",
            "service": "end",
        })
        edges.append({"source": "notification", "target": "end"})

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
            "duplicate_handling": duplicate_handling,
        },
    }

    return {
        "final_workflow": workflow_json,
        "messages": [
            AIMessage(
                content=(
                    f"Workflow generated successfully with "
                    f"{len(nodes)} steps. Check the canvas →"
                )
            )
        ],
    }