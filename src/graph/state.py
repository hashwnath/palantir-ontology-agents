"""Agent state schema for the LangGraph workflow.

Extends LangGraph's MessagesState with ontology-specific fields for
passing data between coordinator and specialist agents.
"""

from __future__ import annotations

from typing import Any, Annotated, Optional
from langgraph.graph import MessagesState
from langchain_core.messages import BaseMessage


import operator


def merge_dict(a: dict, b: dict) -> dict:
    """Merge two dicts, with b overriding a."""
    merged = {**a}
    merged.update(b)
    return merged


def merge_lists(a: list, b: list) -> list:
    """Merge two lists by concatenation, deduplicating by timestamp+agent."""
    seen = set()
    merged = []
    for item in a + b:
        key = (item.get("agent", ""), item.get("timestamp", ""), item.get("status", ""))
        if key not in seen:
            seen.add(key)
            merged.append(item)
    return merged


class AgentState(MessagesState):
    """Shared state across all agents in the workflow.

    Extends MessagesState with typed fields for ontology data,
    agent results, and workflow metadata.
    """
    # Query
    query: str = ""

    # Ontology store (serialized)
    ontology_store_data: Annotated[dict[str, Any], merge_dict] = {}

    # Agent results
    osint_results: Annotated[dict[str, Any], merge_dict] = {}
    graph_results: Annotated[dict[str, Any], merge_dict] = {}
    threat_results: Annotated[dict[str, Any], merge_dict] = {}
    briefing: Annotated[dict[str, Any], merge_dict] = {}

    # Timeline for UI
    timeline: Annotated[list[dict[str, Any]], merge_lists] = []

    # Workflow metadata
    status: str = "initialized"
    error: Optional[str] = None
