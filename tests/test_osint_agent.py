"""Tests for the OSINT Collector agent."""

import pytest
from src.agents.osint_agent import OSINTAgent, OSINTResult


class TestOSINTAgent:
    """Test OSINT collection and entity extraction."""

    def test_run_returns_result(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait supply chain disruption")
        assert isinstance(result, OSINTResult)

    def test_finds_search_results(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait")
        assert result.sources_consulted > 0
        assert len(result.search_results) > 0

    def test_extracts_entities(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait supply chain disruption")
        assert len(result.extracted_entities) > 0

        entity_ids = [e["id"] for e in result.extracted_entities]
        assert "tsmc" in entity_ids or "taiwan_strait" in entity_ids

    def test_extracts_key_findings(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait supply chain disruption")
        assert len(result.key_findings) > 0

    def test_result_serializable(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        result = agent.run("Taiwan Strait")
        d = result.to_dict()
        assert "query" in d
        assert "search_results" in d
        assert "extracted_entities" in d

    def test_runs_without_store(self):
        agent = OSINTAgent()
        result = agent.run("Taiwan Strait")
        assert isinstance(result, OSINTResult)
        assert result.sources_consulted > 0

    def test_multiple_search_queries_generated(self, sample_ontology_store):
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        queries = agent._generate_search_queries("Taiwan Strait supply chain")
        assert len(queries) >= 2

    def test_entity_extraction_from_results(self, sample_ontology_store):
        from src.tools.web_search import SearchResult
        agent = OSINTAgent(ontology_store=sample_ontology_store)
        results = [
            SearchResult(title="TSMC production update", url="http://test.com",
                         content="TSMC in Taiwan Strait region faces challenges from PLA exercises.", score=0.9)
        ]
        entities = agent._extract_entities(results)
        ids = [e["id"] for e in entities]
        assert "tsmc" in ids
