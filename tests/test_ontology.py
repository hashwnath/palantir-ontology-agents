"""Tests for the ontology layer: schema, store, and loader."""

import pytest
from src.ontology.schema import (
    Entity, Organization, Person, Location, Event, Asset, Threat,
    Relationship, RelationshipType, EntityType,
)
from src.ontology.store import OntologyStore
from src.ontology.loader import load_sample_data


class TestEntitySchema:
    """Test entity creation and serialization."""

    def test_create_organization(self):
        org = Organization(id="test", name="Test Corp", org_type="corporation", country="US")
        assert org.name == "Test Corp"
        assert org.entity_type == EntityType.ORGANIZATION
        assert org.org_type == "corporation"

    def test_create_person(self):
        person = Person(id="p1", name="John Doe", role="CEO", nationality="American")
        assert person.entity_type == EntityType.PERSON
        assert person.role == "CEO"

    def test_create_location(self):
        loc = Location(id="l1", name="Test Port", latitude=25.0, longitude=120.0, location_type="port")
        assert loc.entity_type == EntityType.LOCATION
        assert loc.latitude == 25.0

    def test_create_event(self):
        event = Event(id="e1", name="Test Event", event_type="military_exercise", severity="high")
        assert event.entity_type == EntityType.EVENT
        assert event.severity == "high"

    def test_create_asset(self):
        asset = Asset(id="a1", name="Test Ship", asset_type="vessel", operator="Navy")
        assert asset.entity_type == EntityType.ASSET

    def test_create_threat(self):
        threat = Threat(id="t1", name="Test Threat", threat_type="military", likelihood=0.7)
        assert threat.entity_type == EntityType.THREAT
        assert threat.likelihood == 0.7

    def test_entity_to_dict(self):
        org = Organization(id="test", name="Test Corp")
        d = org.to_dict()
        assert d["id"] == "test"
        assert d["name"] == "Test Corp"
        assert d["entity_type"] == "organization"

    def test_relationship_creation(self):
        rel = Relationship(
            id="r1", source_id="a", target_id="b",
            relationship_type=RelationshipType.SUPPLIES,
            weight=0.9,
        )
        assert rel.relationship_type == RelationshipType.SUPPLIES
        assert rel.weight == 0.9


class TestOntologyStore:
    """Test the in-memory ontology store."""

    def test_add_and_get_entity(self, minimal_store):
        entity = minimal_store.get_entity("org1")
        assert entity is not None
        assert entity.name == "Test Org"

    def test_entity_count(self, minimal_store):
        assert minimal_store.entity_count == 3

    def test_relationship_count(self, minimal_store):
        assert minimal_store.relationship_count == 2

    def test_query_by_type(self, minimal_store):
        orgs = minimal_store.query_by_type(EntityType.ORGANIZATION)
        assert len(orgs) == 1
        assert orgs[0].name == "Test Org"

    def test_query_by_attribute(self, minimal_store):
        results = minimal_store.query_by_attribute("country", "US")
        assert len(results) >= 1

    def test_search(self, minimal_store):
        results = minimal_store.search("Test")
        assert len(results) == 3  # All entities have "Test" in name

    def test_get_entity_by_name(self, minimal_store):
        entity = minimal_store.get_entity_by_name("Test Org")
        assert entity is not None
        assert entity.id == "org1"

    def test_get_neighbors(self, minimal_store):
        neighbors = minimal_store.get_neighbors("org1")
        assert len(neighbors) == 1
        neighbor, rel = neighbors[0]
        assert neighbor.id == "loc1"

    def test_traverse(self, minimal_store):
        result = minimal_store.traverse("org1", hops=2)
        assert "org1" in result["entities"]
        assert "loc1" in result["entities"]
        assert result["entity_count"] >= 2

    def test_find_path(self, minimal_store):
        path = minimal_store.find_path("org1", "threat1")
        assert path is not None
        assert path[0] == "org1"
        assert path[-1] == "threat1"

    def test_find_path_same_entity(self, minimal_store):
        path = minimal_store.find_path("org1", "org1")
        assert path == ["org1"]

    def test_find_path_no_path(self):
        store = OntologyStore()
        store.add_entity(Organization(id="a", name="A"))
        store.add_entity(Organization(id="b", name="B"))
        path = store.find_path("a", "b")
        assert path is None

    def test_calculate_exposure_score(self, minimal_store):
        score = minimal_store.calculate_exposure_score("org1")
        assert 0.0 <= score <= 1.0
        assert score > 0  # org1 is connected to threat via loc1

    def test_remove_entity(self, minimal_store):
        assert minimal_store.remove_entity("org1")
        assert minimal_store.get_entity("org1") is None
        assert minimal_store.entity_count == 2

    def test_to_dict(self, minimal_store):
        d = minimal_store.to_dict()
        assert "entities" in d
        assert "relationships" in d
        assert "stats" in d
        assert d["stats"]["entity_count"] == 3


class TestOntologyLoader:
    """Test the sample data loader."""

    def test_loader_returns_store(self):
        store = load_sample_data()
        assert isinstance(store, OntologyStore)

    def test_loader_has_entities(self, sample_ontology_store):
        assert sample_ontology_store.entity_count >= 45

    def test_loader_has_relationships(self, sample_ontology_store):
        assert sample_ontology_store.relationship_count >= 100

    def test_key_entities_present(self, sample_ontology_store):
        tsmc = sample_ontology_store.get_entity("tsmc")
        assert tsmc is not None
        assert tsmc.name == "TSMC"

        strait = sample_ontology_store.get_entity("taiwan_strait")
        assert strait is not None

        navy = sample_ontology_store.get_entity("uspacflt")
        assert navy is not None

    def test_entity_types_diverse(self, sample_ontology_store):
        for et in EntityType:
            entities = sample_ontology_store.query_by_type(et)
            assert len(entities) > 0, f"No entities of type {et.value}"

    def test_tsmc_has_neighbors(self, sample_ontology_store):
        neighbors = sample_ontology_store.get_neighbors("tsmc")
        assert len(neighbors) >= 5  # TSMC has many relationships

    def test_two_hop_traversal(self, sample_ontology_store):
        result = sample_ontology_store.traverse("tsmc", hops=2)
        assert result["entity_count"] >= 10  # Should reach many entities in 2 hops
