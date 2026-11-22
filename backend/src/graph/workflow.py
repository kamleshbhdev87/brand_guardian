'''
This module define the DAG : Directed acyclic graph that orchestrates the video compaliance audit workflow.
it conects the nodes using the StateGraph from LangGrapgh

START -> indrx_video_node -> audit_content_node - > END
'''

from langgraph.graph import StateGraph, END
from backend.src.graph.state import VideoAuditState


from backend.src.graph.nodes import (
    index_video_node,
    audit_content_node
)

def create_graph():
    """
    Constructs and complies the LangGraph workflow
    Returns : 
    Compiled Graph: runnable graph object for execution
    """

    # initialize the graph with state schema
    workflow = StateGraph(VideoAuditState)
    # add the nodes
    workflow.add_node("indexer", index_video_node)
    workflow.add_node("auditor", audit_content_node)
    # define the entry point : indexer
    workflow.set_entry_point("indexer")
    # define the edges
    workflow.add_edge("indexer", "auditor")

    # once the audit is complites the workflow ends
    workflow.add_edge("auditor", END)

    # complie the graph to make it ready for execution
    app=workflow.compile()
    return app

# expose this runnable app
app = create_graph()

