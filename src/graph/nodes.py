"""LangGraph node functions wrapping each specialist agent.

Each node function takes AgentState, runs the corresponding agent,
and returns state updates.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage

from src.graph.state import AgentState
from src.ontology.loader import load_sample_data
from src.ontology.store import OntologyStore
from src.agents.osint_agent import OSINTAgent
from src.agents.graph_agent import GraphAnalystAgent
from src.agents.threat_agent import ThreatAssessorAgent, ThreatAssessmentResult
from src.agents.briefing_agent import BriefingDrafterAgent, BriefingResult
from src.agents.osint_agent import OSINTResult
from src.agents.graph_agent import GraphAnalysisResult


def _get_store(state: AgentState) -> OntologyStore:
    """Reconstruct or load the ontology store from state."""
    # Always load fresh sample data for the demo
    return load_sample_data()


def _timeline_entry(agent: str, status: str, detail: str = "") -> dict[str, Any]:
    return {
        "agent": agent,
        "status": status,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat(),
    }


def coordinator_node(state: AgentState) -> dict[str, Any]:
    """Coordinator node: initializes the workflow and prepares the ontology.

    Routes the query to parallel OSINT and Graph Analyst agents.
    """
    query = state.get("query", "") or ""
    if not query:
        # Extract query from last human message
        for msg in reversed(state.get("messages", [])):
            if hasattr(msg, "type") and msg.type == "human":
                query = msg.content
                break

    store = load_sample_data()

    timeline = state.get("timeline", []) or []
    timeline.append(_timeline_entry("coordinator", "started", f"Processing: {query[:80]}"))
    timeline.append(_timeline_entry("coordinator", "completed", f"Ontology loaded: {store.entity_count} entities, {store.relationship_count} relationships"))

    return {
        "query": query,
        "ontology_store_data": store.to_dict(),
        "timeline": timeline,
        "status": "coordinator_complete",
        "messages": [AIMessage(content=f"[Coordinator] Initialized ontology with {store.entity_count} entities. Dispatching OSINT and Graph Analyst agents for: {query[:100]}")],
    }


def osint_node(state: AgentState) -> dict[str, Any]:
    """OSINT Collector node: searches web and extracts intelligence."""
    query = state.get("query", "Taiwan Strait supply chain disruption")
    store = _get_store(state)

    timeline = state.get("timeline", []) or []
    timeline.append(_timeline_entry("osint_collector", "started", "Web search initiated"))

    agent = OSINTAgent(ontology_store=store)
    result = agent.run(query)

    timeline.append(_timeline_entry(
        "osint_collector", "completed",
        f"Found {result.sources_consulted} sources, extracted {len(result.extracted_entities)} entities"
    ))

    return {
        "osint_results": result.to_dict(),
        "timeline": timeline,
        "messages": [AIMessage(content=f"[OSINT Collector] Collected {result.sources_consulted} sources. Key findings: {'; '.join(result.key_findings[:3])}")],
    }


def graph_analyst_node(state: AgentState) -> dict[str, Any]:
    """Graph Analyst node: traverses ontology and analyzes relationships."""
    query = state.get("query", "Taiwan Strait supply chain disruption")
    store = _get_store(state)

    timeline = state.get("timeline", []) or []
    timeline.append(_timeline_entry("graph_analyst", "started", "Ontology traversal initiated"))

    agent = GraphAnalystAgent(ontology_store=store)
    result = agent.run(query)

    timeline.append(_timeline_entry(
        "graph_analyst", "completed",
        f"Analyzed {len(result.exposure_scores)} entities, found {len(result.dependency_chains)} dependency chains"
    ))

    return {
        "graph_results": result.to_dict(),
        "timeline": timeline,
        "messages": [AIMessage(content=f"[Graph Analyst] Analysis complete. Key findings: {'; '.join(result.key_findings[:3])}")],
    }


def threat_assessor_node(state: AgentState) -> dict[str, Any]:
    """Threat Assessor node: evaluates threats and calculates risk scores."""
    query = state.get("query", "Taiwan Strait supply chain disruption")

    timeline = state.get("timeline", []) or []
    timeline.append(_timeline_entry("threat_assessor", "started", "Threat assessment initiated"))

    # Reconstruct upstream results
    osint_data = state.get("osint_results", {})
    graph_data = state.get("graph_results", {})

    osint_result = None
    if osint_data:
        osint_result = OSINTResult(**{k: v for k, v in osint_data.items() if k in OSINTResult.__dataclass_fields__})

    graph_result = None
    if graph_data:
        graph_result = GraphAnalysisResult(**{k: v for k, v in graph_data.items() if k in GraphAnalysisResult.__dataclass_fields__})

    agent = ThreatAssessorAgent()
    result = agent.run(query, osint_result=osint_result, graph_result=graph_result)

    timeline.append(_timeline_entry(
        "threat_assessor", "completed",
        f"Risk level: {result.overall_risk_level} (score: {result.overall_risk_score:.2f})"
    ))

    return {
        "threat_results": result.to_dict(),
        "timeline": timeline,
        "messages": [AIMessage(content=f"[Threat Assessor] Risk level: {result.overall_risk_level} (score: {result.overall_risk_score:.2f}, confidence: {result.confidence:.2f})")],
    }


def briefing_drafter_node(state: AgentState) -> dict[str, Any]:
    """Briefing Drafter node: generates executive briefing from all results."""
    query = state.get("query", "Taiwan Strait supply chain disruption")

    timeline = state.get("timeline", []) or []
    timeline.append(_timeline_entry("briefing_drafter", "started", "Briefing generation initiated"))

    # Reconstruct upstream results
    osint_data = state.get("osint_results", {})
    graph_data = state.get("graph_results", {})
    threat_data = state.get("threat_results", {})

    osint_result = None
    if osint_data:
        osint_result = OSINTResult(**{k: v for k, v in osint_data.items() if k in OSINTResult.__dataclass_fields__})

    graph_result = None
    if graph_data:
        graph_result = GraphAnalysisResult(**{k: v for k, v in graph_data.items() if k in GraphAnalysisResult.__dataclass_fields__})

    threat_result = None
    if threat_data:
        threat_result = ThreatAssessmentResult(**{k: v for k, v in threat_data.items() if k in ThreatAssessmentResult.__dataclass_fields__})

    agent = BriefingDrafterAgent()
    result = agent.run(query, osint_result=osint_result, graph_result=graph_result, threat_result=threat_result)

    timeline.append(_timeline_entry("briefing_drafter", "completed", "Executive briefing generated"))

    return {
        "briefing": result.to_dict(),
        "timeline": timeline,
        "status": "complete",
        "messages": [AIMessage(content=f"[Briefing Drafter] Executive briefing generated. Risk level: {result.metadata.get('threat_level', 'N/A')}")],
    }
