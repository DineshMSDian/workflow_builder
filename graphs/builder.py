from langgraph.graph import StateGraph, END
from graphs.state_schema import WorkflowState
from graphs.edges import check_uncertainty, check_missing_info
from nodes.understand_intent import understand_intent
from nodes.extract_info import extract_info
from nodes.ask_clarification import ask_clarification
from nodes.process_clarification import process_clarification_response
from nodes.generate_workflow import generate_workflow
from functools import partial

def build_graph(llm):
    graph = StateGraph(WorkflowState)

    # binding llm with the nodes which ecpects it
    graph.add_node('understand_intent', partial(understand_intent, llm=llm))
    graph.add_node('extract_info', extract_info)
    graph.add_node('ask_clarification', partial(ask_clarification, llm=llm))
    graph.add_node('process_clarification_response', partial(process_clarification_response, llm=llm))
    graph.add_node('generate_workflow', partial(generate_workflow, llm=llm))

    graph.set_entry_point('understand_intent')

    graph.add_edge('understand_intent', 'extract_info')
    graph.add_conditional_edges('extract_info', check_missing_info)
    graph.add_edge('ask_clarification', 'process_clarification_response')
    graph.add_conditional_edges('preprocess_clarification_response', check_uncertainty)
    graph.add_edge('generate_workflow', END)

    return graph.compile()