"""Shared test fixtures for the multi-agent ontology workflow tests."""

from __future__ import annotations

from unittest.mock import MagicMock
import pytest

from src.ontology.loader import load_sample_data
from src.ontology.store import OntologyStore
from src.ontology.schema import (
    Organization, Person, Location, Event, Asset, Threat,
    Relationship, RelationshipType, EntityType,
)
from src.agents.osint_agent import OSINTResult
from src.agents.graph_agent import GraphAnalysisResult
from src.agents.threat_agent import ThreatAssessmentResult
from src.agents.briefing_agent import BriefingResult


@pytest.fixture
def mock_llm():
    """Create a mock LLM that returns predictable responses."""
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="Mock LLM response for testing.")
    return llm


@pytest.fixture
def sample_ontology_store() -> OntologyStore:
    """Load the full sample ontology store."""
    return load_sample_data()


@pytest.fixture
def minimal_store() -> OntologyStore:
    """Create a minimal ontology store for focused tests."""
    store = OntologyStore()
    org = Organization(id="org1", name="Test Org", org_type="corporation", country="US")
    loc = Location(id="loc1", name="Test Port", location_type="port", country="US")
    threat = Threat(id="threat1", name="Test Threat", threat_type="military", severity="high", likelihood=0.7)

    store.add_entity(org)
    store.add_entity(loc)
    store.add_entity(threat)

    store.add_relationship(Relationship(
        id="rel1", source_id="org1", target_id="loc1",
        relationship_type=RelationshipType.OPERATES_IN,
    ))
    store.add_relationship(Relationship(
        id="rel2", source_id="threat1", target_id="loc1",
        relationship_type=RelationshipType.THREATENS,
    ))
    return store


@pytest.fixture
def sample_osint_result() -> OSINTResult:
    """Create a sample OSINT result."""
    return OSINTResult(
        query="Taiwan Strait supply chain disruption",
        search_results=[
            {"title": "PLA Exercises Around Taiwan", "url": "https://example.com/1",
             "content": "Large-scale PLA military exercises...", "score": 0.95},
        ],
        extracted_entities=[
            {"id": "tsmc", "name": "TSMC", "type": "organization", "mention_count": 3},
            {"id": "taiwan_strait", "name": "Taiwan Strait", "type": "location", "mention_count": 5},
        ],
        key_findings=[
            "PLA launched Joint Sword-2026A exercises around Taiwan.",
            "TSMC warns of potential production delays.",
        ],
        sources_consulted=5,
    )


@pytest.fixture
def sample_graph_result() -> GraphAnalysisResult:
    """Create a sample graph analysis result."""
    return GraphAnalysisResult(
        query="Taiwan Strait supply chain disruption",
        dependency_chains=[
            [{"id": "apple", "name": "Apple Inc."}, {"id": "tsmc", "name": "TSMC"},
             {"id": "taiwan_strait", "name": "Taiwan Strait"}],
        ],
        exposure_scores=[
            {"entity_id": "tsmc", "name": "TSMC", "type": "organization", "exposure_score": 0.95},
            {"entity_id": "apple", "name": "Apple Inc.", "type": "organization", "exposure_score": 0.75},
        ],
        hub_entities=[
            {"id": "taiwan_strait", "name": "Taiwan Strait", "type": "location", "degree": 25},
        ],
        key_findings=["Taiwan Strait is the most connected entity with 25 relationships."],
    )


@pytest.fixture
def sample_threat_result() -> ThreatAssessmentResult:
    """Create a sample threat assessment result."""
    return ThreatAssessmentResult(
        query="Taiwan Strait supply chain disruption",
        overall_risk_score=0.78,
        overall_risk_level="HIGH",
        confidence=0.80,
        threat_assessments=[
            {"threat_id": "TI-001", "category": "military_buildup", "severity": "critical", "confidence": 0.87},
        ],
        key_findings=["Overall risk level: HIGH (score: 0.78, confidence: 0.80)"],
    )
