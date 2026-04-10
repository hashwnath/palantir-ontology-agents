"""Tests for the Briefing Drafter agent."""

import pytest
from src.agents.briefing_agent import BriefingDrafterAgent, BriefingResult


class TestBriefingDrafterAgent:
    """Test executive briefing generation."""

    def test_run_returns_result(self):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait supply chain disruption")
        assert isinstance(result, BriefingResult)

    def test_generates_briefing_text(self):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait")
        assert len(result.briefing_text) > 0
        assert "EXECUTIVE INTELLIGENCE BRIEFING" in result.briefing_text

    def test_has_all_sections(self):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait")
        required_sections = [
            "executive_summary", "key_findings", "risk_assessment",
            "recommendations", "outlook",
        ]
        for section in required_sections:
            assert section in result.sections, f"Missing section: {section}"
            assert len(result.sections[section]) > 0

    def test_with_all_agent_results(self, sample_osint_result, sample_graph_result, sample_threat_result):
        agent = BriefingDrafterAgent()
        result = agent.run(
            "Taiwan Strait supply chain disruption",
            osint_result=sample_osint_result,
            graph_result=sample_graph_result,
            threat_result=sample_threat_result,
        )
        assert isinstance(result, BriefingResult)
        assert "HIGH" in result.briefing_text or "CRITICAL" in result.briefing_text

    def test_metadata_populated(self, sample_osint_result, sample_graph_result, sample_threat_result):
        agent = BriefingDrafterAgent()
        result = agent.run(
            "Taiwan Strait",
            osint_result=sample_osint_result,
            graph_result=sample_graph_result,
            threat_result=sample_threat_result,
        )
        assert result.metadata["osint_sources"] == 5
        assert result.metadata["threat_level"] == "HIGH"

    def test_handles_partial_results(self, sample_osint_result):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait", osint_result=sample_osint_result)
        assert isinstance(result, BriefingResult)
        assert len(result.briefing_text) > 0

    def test_handles_no_results(self):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait")
        assert isinstance(result, BriefingResult)
        assert "pending" in result.briefing_text.lower() or "UNDETERMINED" in result.briefing_text

    def test_result_serializable(self):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait")
        d = result.to_dict()
        assert "briefing_text" in d
        assert "sections" in d
        assert "metadata" in d

    def test_briefing_has_recommendations(self, sample_threat_result):
        agent = BriefingDrafterAgent()
        result = agent.run("Taiwan Strait", threat_result=sample_threat_result)
        recs = result.sections.get("recommendations", "")
        assert "IMMEDIATE" in recs
        assert "SHORT-TERM" in recs
