"""Tests for the Orchestrator."""

import pytest
from unittest.mock import patch, MagicMock
from src.orchestrator import Orchestrator


class TestOrchestrator:
    """Test the orchestrator initialization and execution."""

    def test_init_default(self):
        orch = Orchestrator()
        assert orch.model_name == "claude-sonnet-4-20250514"

    def test_init_custom_model(self):
        orch = Orchestrator(model_name="claude-opus-4-20250514")
        assert orch.model_name == "claude-opus-4-20250514"

    def test_workflow_builds(self):
        orch = Orchestrator()
        workflow = orch.workflow
        assert workflow is not None

    def test_run_executes(self):
        """Test that run() executes the full workflow."""
        orch = Orchestrator()
        result = orch.run("Taiwan Strait supply chain disruption")

        # Should have all result sections
        assert "osint_results" in result
        assert "graph_results" in result
        assert "threat_results" in result
        assert "briefing" in result

    def test_run_populates_osint(self):
        orch = Orchestrator()
        result = orch.run("Taiwan Strait")
        osint = result.get("osint_results", {})
        assert osint.get("sources_consulted", 0) > 0

    def test_run_populates_graph(self):
        orch = Orchestrator()
        result = orch.run("Taiwan Strait supply chain")
        graph = result.get("graph_results", {})
        assert len(graph.get("exposure_scores", [])) > 0

    def test_run_populates_threat(self):
        orch = Orchestrator()
        result = orch.run("Taiwan Strait")
        threat = result.get("threat_results", {})
        assert threat.get("overall_risk_score", 0) > 0

    def test_run_populates_briefing(self):
        orch = Orchestrator()
        result = orch.run("Taiwan Strait")
        briefing = result.get("briefing", {})
        assert len(briefing.get("briefing_text", "")) > 0

    def test_run_has_timeline(self):
        orch = Orchestrator()
        result = orch.run("Taiwan Strait")
        timeline = result.get("timeline", [])
        assert len(timeline) > 0

    def test_run_stream(self):
        orch = Orchestrator()
        events = list(orch.run_stream("Taiwan Strait"))
        assert len(events) > 0
        node_names = [name for name, _ in events]
        assert "coordinator" in node_names
        assert "briefing_drafter" in node_names
