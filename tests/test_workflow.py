"""Tests for the LangGraph workflow."""

import pytest
from langchain_core.messages import HumanMessage

from src.graph.workflow import build_workflow
from src.graph.state import AgentState


class TestWorkflow:
    """Test the LangGraph workflow definition and execution."""

    def test_workflow_compiles(self):
        workflow = build_workflow()
        assert workflow is not None

    def test_workflow_full_execution(self):
        """Test full workflow execution with demo data."""
        workflow = build_workflow()

        initial_state = {
            "messages": [HumanMessage(content="Taiwan Strait supply chain disruption")],
            "query": "Taiwan Strait supply chain disruption",
            "ontology_store_data": {},
            "osint_results": {},
            "graph_results": {},
            "threat_results": {},
            "briefing": {},
            "timeline": [],
            "status": "started",
            "error": None,
        }

        result = workflow.invoke(initial_state)

        # Verify all agents ran
        assert result["osint_results"] != {}
        assert result["graph_results"] != {}
        assert result["threat_results"] != {}
        assert result["briefing"] != {}

    def test_workflow_streaming(self):
        """Test workflow streaming output."""
        workflow = build_workflow()

        initial_state = {
            "messages": [HumanMessage(content="Taiwan Strait")],
            "query": "Taiwan Strait",
            "ontology_store_data": {},
            "osint_results": {},
            "graph_results": {},
            "threat_results": {},
            "briefing": {},
            "timeline": [],
            "status": "started",
            "error": None,
        }

        events = list(workflow.stream(initial_state))
        assert len(events) > 0

        # Check that we see expected nodes
        node_names = set()
        for event in events:
            node_names.update(event.keys())

        assert "coordinator" in node_names
        assert "osint_collector" in node_names
        assert "graph_analyst" in node_names
        assert "threat_assessor" in node_names
        assert "briefing_drafter" in node_names

    def test_parallel_agents_both_complete(self):
        """Verify both parallel agents (OSINT + Graph) complete."""
        workflow = build_workflow()

        initial_state = {
            "messages": [HumanMessage(content="Taiwan Strait")],
            "query": "Taiwan Strait",
            "ontology_store_data": {},
            "osint_results": {},
            "graph_results": {},
            "threat_results": {},
            "briefing": {},
            "timeline": [],
            "status": "started",
            "error": None,
        }

        result = workflow.invoke(initial_state)

        # Both parallel agents should have produced results
        assert result["osint_results"].get("sources_consulted", 0) > 0
        assert len(result["graph_results"].get("exposure_scores", [])) > 0

    def test_state_passes_through_correctly(self):
        """Verify state passes correctly between sequential agents."""
        workflow = build_workflow()

        initial_state = {
            "messages": [HumanMessage(content="Taiwan Strait")],
            "query": "Taiwan Strait",
            "ontology_store_data": {},
            "osint_results": {},
            "graph_results": {},
            "threat_results": {},
            "briefing": {},
            "timeline": [],
            "status": "started",
            "error": None,
        }

        result = workflow.invoke(initial_state)

        # Briefing should reference threat level from threat assessor
        briefing = result.get("briefing", {})
        metadata = briefing.get("metadata", {})
        assert metadata.get("threat_level") in ["CRITICAL", "HIGH", "ELEVATED", "GUARDED", "LOW"]
        assert metadata.get("risk_score", 0) > 0

    def test_workflow_status_complete(self):
        workflow = build_workflow()
        initial_state = {
            "messages": [HumanMessage(content="Taiwan Strait")],
            "query": "Taiwan Strait",
            "ontology_store_data": {},
            "osint_results": {},
            "graph_results": {},
            "threat_results": {},
            "briefing": {},
            "timeline": [],
            "status": "started",
            "error": None,
        }
        result = workflow.invoke(initial_state)
        assert result["status"] == "complete"
