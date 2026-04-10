"""LangGraph workflow definition.

Defines the StateGraph: START -> coordinator -> [osint, graph_analyst] (parallel) -> threat_assessor -> briefing_drafter -> END
"""

from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from src.graph.state import AgentState
from src.graph.nodes import (
    coordinator_node,
    osint_node,
    graph_analyst_node,
    threat_assessor_node,
    briefing_drafter_node,
)


def build_workflow() -> StateGraph:
    """Build and compile the multi-agent workflow graph.

    Architecture:
        START -> coordinator -> [osint_collector, graph_analyst] (parallel)
              -> threat_assessor -> briefing_drafter -> END

    Returns:
        Compiled LangGraph StateGraph ready for execution.
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("osint_collector", osint_node)
    graph.add_node("graph_analyst", graph_analyst_node)
    graph.add_node("threat_assessor", threat_assessor_node)
    graph.add_node("briefing_drafter", briefing_drafter_node)

    # Define edges
    # START -> coordinator
    graph.add_edge(START, "coordinator")

    # coordinator -> parallel branch (osint + graph_analyst)
    graph.add_edge("coordinator", "osint_collector")
    graph.add_edge("coordinator", "graph_analyst")

    # Both parallel agents -> threat_assessor
    graph.add_edge("osint_collector", "threat_assessor")
    graph.add_edge("graph_analyst", "threat_assessor")

    # threat_assessor -> briefing_drafter -> END
    graph.add_edge("threat_assessor", "briefing_drafter")
    graph.add_edge("briefing_drafter", END)

    return graph.compile()
