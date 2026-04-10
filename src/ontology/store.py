"""In-memory ontology store with graph traversal, querying, and relationship management."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Optional

from src.ontology.schema import Entity, EntityType, Relationship, RelationshipType


class OntologyStore:
    """In-memory graph store for ontology objects.

    Supports typed entity storage, relationship management, N-hop graph traversal,
    and attribute-based querying. Designed to mirror Palantir Ontology patterns.
    """

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}
        self._relationships: dict[str, Relationship] = {}
        # Adjacency lists for fast traversal
        self._outgoing: dict[str, list[str]] = defaultdict(list)  # entity_id -> [rel_id]
        self._incoming: dict[str, list[str]] = defaultdict(list)  # entity_id -> [rel_id]
        # Type index
        self._type_index: dict[EntityType, set[str]] = defaultdict(set)

    # --- Entity operations ---

    def add_entity(self, entity: Entity) -> str:
        """Add an entity to the store. Returns entity ID."""
        self._entities[entity.id] = entity
        self._type_index[entity.entity_type].add(entity.id)
        return entity.id

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Retrieve an entity by ID."""
        return self._entities.get(entity_id)

    def get_entity_by_name(self, name: str) -> Optional[Entity]:
        """Find first entity matching the given name (case-insensitive)."""
        name_lower = name.lower()
        for entity in self._entities.values():
            if entity.name.lower() == name_lower:
                return entity
        return None

    def remove_entity(self, entity_id: str) -> bool:
        """Remove an entity and all its relationships."""
        if entity_id not in self._entities:
            return False
        entity = self._entities.pop(entity_id)
        self._type_index[entity.entity_type].discard(entity_id)
        # Remove associated relationships
        rel_ids = set(self._outgoing.pop(entity_id, []) + self._incoming.pop(entity_id, []))
        for rid in rel_ids:
            self._relationships.pop(rid, None)
        return True

    # --- Relationship operations ---

    def add_relationship(self, relationship: Relationship) -> str:
        """Add a relationship between two entities. Returns relationship ID."""
        self._relationships[relationship.id] = relationship
        self._outgoing[relationship.source_id].append(relationship.id)
        self._incoming[relationship.target_id].append(relationship.id)
        if relationship.bidirectional:
            self._outgoing[relationship.target_id].append(relationship.id)
            self._incoming[relationship.source_id].append(relationship.id)
        return relationship.id

    def get_relationship(self, rel_id: str) -> Optional[Relationship]:
        """Retrieve a relationship by ID."""
        return self._relationships.get(rel_id)

    # --- Query operations ---

    def query_by_type(self, entity_type: EntityType) -> list[Entity]:
        """Return all entities of a given type."""
        return [self._entities[eid] for eid in self._type_index.get(entity_type, set())
                if eid in self._entities]

    def query_by_attribute(self, key: str, value: Any) -> list[Entity]:
        """Return entities where attributes[key] == value or top-level field matches."""
        results = []
        for entity in self._entities.values():
            if entity.attributes.get(key) == value:
                results.append(entity)
            elif hasattr(entity, key) and getattr(entity, key) == value:
                results.append(entity)
        return results

    def search(self, query: str) -> list[Entity]:
        """Full-text search across entity names and descriptions."""
        query_lower = query.lower()
        results = []
        for entity in self._entities.values():
            if query_lower in entity.name.lower() or query_lower in entity.description.lower():
                results.append(entity)
        return results

    # --- Graph traversal ---

    def get_neighbors(self, entity_id: str, relationship_type: Optional[RelationshipType] = None,
                      direction: str = "both") -> list[tuple[Entity, Relationship]]:
        """Get immediate neighbors of an entity, optionally filtered by relationship type.

        Args:
            entity_id: The entity to find neighbors for.
            relationship_type: Optional filter for relationship type.
            direction: 'outgoing', 'incoming', or 'both'.

        Returns:
            List of (neighbor_entity, relationship) tuples.
        """
        neighbors: list[tuple[Entity, Relationship]] = []
        rel_ids: set[str] = set()

        if direction in ("outgoing", "both"):
            rel_ids.update(self._outgoing.get(entity_id, []))
        if direction in ("incoming", "both"):
            rel_ids.update(self._incoming.get(entity_id, []))

        for rid in rel_ids:
            rel = self._relationships.get(rid)
            if rel is None:
                continue
            if relationship_type and rel.relationship_type != relationship_type:
                continue
            # Determine the neighbor
            if rel.source_id == entity_id:
                neighbor_id = rel.target_id
            else:
                neighbor_id = rel.source_id
            neighbor = self._entities.get(neighbor_id)
            if neighbor:
                neighbors.append((neighbor, rel))

        return neighbors

    def traverse(self, entity_id: str, hops: int = 2,
                 relationship_type: Optional[RelationshipType] = None) -> dict[str, Any]:
        """Traverse the graph from an entity up to N hops.

        Returns a dict with 'entities' (set of reached entity IDs),
        'relationships' (set of traversed relationship IDs),
        and 'paths' (list of paths as entity ID sequences).
        """
        visited_entities: set[str] = {entity_id}
        visited_rels: set[str] = set()
        paths: list[list[str]] = [[entity_id]]
        frontier = [(entity_id, [entity_id], 0)]

        while frontier:
            current_id, current_path, depth = frontier.pop(0)
            if depth >= hops:
                continue
            for neighbor, rel in self.get_neighbors(current_id, relationship_type):
                visited_rels.add(rel.id)
                new_path = current_path + [neighbor.id]
                if neighbor.id not in visited_entities:
                    visited_entities.add(neighbor.id)
                    paths.append(new_path)
                    frontier.append((neighbor.id, new_path, depth + 1))

        return {
            "root": entity_id,
            "hops": hops,
            "entities": visited_entities,
            "relationships": visited_rels,
            "paths": paths,
            "entity_count": len(visited_entities),
            "relationship_count": len(visited_rels),
        }

    def find_path(self, source_id: str, target_id: str, max_hops: int = 5) -> Optional[list[str]]:
        """BFS shortest path between two entities."""
        if source_id == target_id:
            return [source_id]
        visited = {source_id}
        queue = [(source_id, [source_id])]
        while queue:
            current, path = queue.pop(0)
            if len(path) > max_hops + 1:
                break
            for neighbor, _ in self.get_neighbors(current):
                if neighbor.id == target_id:
                    return path + [neighbor.id]
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append((neighbor.id, path + [neighbor.id]))
        return None

    def get_dependency_chains(self, entity_id: str, rel_types: Optional[list[RelationshipType]] = None,
                              max_depth: int = 5) -> list[list[str]]:
        """Find all dependency chains from an entity following specific relationship types."""
        if rel_types is None:
            rel_types = [RelationshipType.DEPENDS_ON, RelationshipType.SUPPLIES,
                         RelationshipType.SUPPLIES_TO]
        chains: list[list[str]] = []
        stack = [(entity_id, [entity_id])]
        while stack:
            current, path = stack.pop()
            if len(path) > max_depth + 1:
                continue
            extended = False
            for neighbor, rel in self.get_neighbors(current, direction="outgoing"):
                if rel.relationship_type in rel_types and neighbor.id not in path:
                    stack.append((neighbor.id, path + [neighbor.id]))
                    extended = True
            if not extended and len(path) > 1:
                chains.append(path)
        return chains

    def calculate_exposure_score(self, entity_id: str, threat_ids: Optional[list[str]] = None) -> float:
        """Calculate exposure score for an entity based on proximity to threats.

        Score is 0.0-1.0 based on hop distance to threat entities and relationship weights.
        """
        if threat_ids is None:
            threat_ids = [e.id for e in self.query_by_type(EntityType.THREAT)]

        if not threat_ids:
            return 0.0

        max_score = 0.0
        for tid in threat_ids:
            path = self.find_path(entity_id, tid)
            if path:
                hop_distance = len(path) - 1
                score = max(0, 1.0 - (hop_distance - 1) * 0.2)
                max_score = max(max_score, score)

        return round(max_score, 2)

    # --- Serialization ---

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entire store to a dictionary."""
        return {
            "entities": {eid: e.to_dict() for eid, e in self._entities.items()},
            "relationships": {rid: r.to_dict() for rid, r in self._relationships.items()},
            "stats": {
                "entity_count": len(self._entities),
                "relationship_count": len(self._relationships),
                "type_distribution": {
                    t.value: len(ids) for t, ids in self._type_index.items() if ids
                },
            },
        }

    @property
    def entity_count(self) -> int:
        return len(self._entities)

    @property
    def relationship_count(self) -> int:
        return len(self._relationships)

    def all_entities(self) -> list[Entity]:
        return list(self._entities.values())

    def all_relationships(self) -> list[Relationship]:
        return list(self._relationships.values())
