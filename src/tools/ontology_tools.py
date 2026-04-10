"""Ontology query and traversal tools for agent use.

LIVE: Provides typed access to the ontology store for querying entities,
traversing relationships, and analyzing graph structure.
"""

from __future__ import annotations

from typing import Any, Optional

from src.ontology.schema import EntityType, RelationshipType
from src.ontology.store import OntologyStore


def query_entities(store: OntologyStore, entity_type: Optional[str] = None,
                   search_term: Optional[str] = None) -> list[dict[str, Any]]:
    """Query entities from the ontology store.

    Args:
        store: The ontology store to query.
        entity_type: Optional entity type filter (organization, person, location, etc.).
        search_term: Optional text search across names and descriptions.

    Returns:
        List of entity dictionaries.
    """
    if entity_type:
        et = EntityType(entity_type.lower())
        entities = store.query_by_type(et)
    elif search_term:
        entities = store.search(search_term)
    else:
        entities = store.all_entities()

    return [e.to_dict() for e in entities]


def traverse_entity(store: OntologyStore, entity_id: str, hops: int = 2,
                    relationship_type: Optional[str] = None) -> dict[str, Any]:
    """Traverse the ontology graph from a starting entity.

    Args:
        store: The ontology store.
        entity_id: Starting entity ID.
        hops: Number of hops to traverse (default 2).
        relationship_type: Optional filter for relationship type.

    Returns:
        Traversal result with entities, relationships, and paths.
    """
    rel_type = RelationshipType(relationship_type) if relationship_type else None
    result = store.traverse(entity_id, hops=hops, relationship_type=rel_type)

    # Enrich with entity names
    enriched_paths = []
    for path in result["paths"]:
        named_path = []
        for eid in path:
            entity = store.get_entity(eid)
            named_path.append({"id": eid, "name": entity.name if entity else "unknown"})
        enriched_paths.append(named_path)

    result["named_paths"] = enriched_paths
    result["entities"] = list(result["entities"])
    result["relationships"] = list(result["relationships"])
    return result


def find_dependency_chains(store: OntologyStore, entity_id: str,
                           max_depth: int = 5) -> list[list[dict[str, str]]]:
    """Find supply chain / dependency chains from an entity.

    Args:
        store: The ontology store.
        entity_id: Starting entity ID.
        max_depth: Maximum chain length.

    Returns:
        List of chains, each chain is a list of {id, name} dicts.
    """
    chains = store.get_dependency_chains(entity_id, max_depth=max_depth)
    named_chains = []
    for chain in chains:
        named_chain = []
        for eid in chain:
            entity = store.get_entity(eid)
            named_chain.append({"id": eid, "name": entity.name if entity else eid})
        named_chains.append(named_chain)
    return named_chains


def get_exposure_report(store: OntologyStore, entity_ids: Optional[list[str]] = None) -> list[dict[str, Any]]:
    """Calculate exposure scores for entities.

    Args:
        store: The ontology store.
        entity_ids: Specific entity IDs to assess. If None, assesses all organizations.

    Returns:
        List of {entity_id, name, exposure_score} sorted by score descending.
    """
    if entity_ids is None:
        entities = store.query_by_type(EntityType.ORGANIZATION)
        entity_ids = [e.id for e in entities]

    report = []
    for eid in entity_ids:
        entity = store.get_entity(eid)
        if entity:
            score = store.calculate_exposure_score(eid)
            report.append({
                "entity_id": eid,
                "name": entity.name,
                "type": entity.entity_type.value,
                "exposure_score": score,
            })

    report.sort(key=lambda x: x["exposure_score"], reverse=True)
    return report


def find_shortest_path(store: OntologyStore, source_id: str, target_id: str) -> Optional[list[dict[str, str]]]:
    """Find shortest path between two entities.

    Args:
        store: The ontology store.
        source_id: Source entity ID.
        target_id: Target entity ID.

    Returns:
        List of {id, name} dicts representing the path, or None.
    """
    path = store.find_path(source_id, target_id)
    if path is None:
        return None
    return [{"id": eid, "name": store.get_entity(eid).name if store.get_entity(eid) else eid} for eid in path]
