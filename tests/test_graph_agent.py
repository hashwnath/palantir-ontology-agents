"""Tests for the Graph Analyst agent."""

import pytest
from src.agents.graph_agent import GraphAnalystAgent, GraphAnalysisResult


class TestGraphAnalystAgent:
    """Test graph traversal and analysis."""

    def test_run_returns_result(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait supply chain disruption")
        assert isinstance(result, GraphAnalysisResult)

    def test_finds_dependency_chains(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan semiconductor supply chain")
        assert len(result.dependency_chains) > 0

    def test_calculates_exposure_scores(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait")
        assert len(result.exposure_scores) > 0
        # At least some entities should have nonzero exposure
        nonzero = [e for e in result.exposure_scores if e["exposure_score"] > 0]
        assert len(nonzero) > 0

    def test_finds_hub_entities(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait")
        assert len(result.hub_entities) > 0
        # Hub entities should be sorted by degree
        degrees = [h["degree"] for h in result.hub_entities]
        assert degrees == sorted(degrees, reverse=True)

    def test_finds_critical_paths(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait military")
        assert len(result.critical_paths) > 0

    def test_generates_key_findings(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait supply chain")
        assert len(result.key_findings) > 0

    def test_traversal_stats(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait")
        assert "total_entities" in result.traversal_stats
        assert "total_relationships" in result.traversal_stats
        assert result.traversal_stats["total_entities"] >= 45

    def test_result_serializable(self, sample_ontology_store):
        agent = GraphAnalystAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan")
        d = result.to_dict()
        assert "dependency_chains" in d
        assert "exposure_scores" in d

    def test_runs_without_store(self):
        agent = GraphAnalystAgent()
        result = agent.run("Taiwan")
        assert isinstance(result, GraphAnalysisResult)
        assert "No ontology store available" in result.key_findings
