"""OSINT Collector Agent - Open-source intelligence collection and entity extraction.

LIVE: Uses Tavily web search (or demo fallback) to collect open-source intelligence,
extracts structured entities from results, and updates the ontology store with new findings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from src.ontology.schema import Entity, EntityType, Relationship, RelationshipType
from src.ontology.store import OntologyStore
from src.tools.web_search import SearchResult, search_web


@dataclass
class OSINTResult:
    """Result from OSINT collection run."""
    query: str = ""
    search_results: list[dict[str, Any]] = field(default_factory=list)
    extracted_entities: list[dict[str, Any]] = field(default_factory=list)
    new_relationships: list[dict[str, Any]] = field(default_factory=list)
    key_findings: list[str] = field(default_factory=list)
    sources_consulted: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "search_results": self.search_results,
            "extracted_entities": self.extracted_entities,
            "new_relationships": self.new_relationships,
            "key_findings": self.key_findings,
            "sources_consulted": self.sources_consulted,
            "timestamp": self.timestamp,
        }


# Entity extraction patterns - keywords mapped to entity types and IDs
ENTITY_PATTERNS: dict[str, dict[str, str]] = {
    "tsmc": {"id": "tsmc", "type": "organization"},
    "taiwan semiconductor": {"id": "tsmc", "type": "organization"},
    "apple": {"id": "apple", "type": "organization"},
    "nvidia": {"id": "nvidia", "type": "organization"},
    "asml": {"id": "asml", "type": "organization"},
    "maersk": {"id": "maersk", "type": "organization"},
    "evergreen": {"id": "evergreen", "type": "organization"},
    "yang ming": {"id": "yang_ming", "type": "organization"},
    "cosco": {"id": "cosco", "type": "organization"},
    "pla": {"id": "pla_navy", "type": "organization"},
    "eastern theater": {"id": "pla_eastern", "type": "organization"},
    "us navy": {"id": "uspacflt", "type": "organization"},
    "pacific fleet": {"id": "uspacflt", "type": "organization"},
    "indo-pacific command": {"id": "uspacflt", "type": "organization"},
    "samsung": {"id": "samsung_semi", "type": "organization"},
    "intel foundry": {"id": "intel_foundry", "type": "organization"},
    "taiwan strait": {"id": "taiwan_strait", "type": "location"},
    "kaohsiung": {"id": "kaohsiung_port", "type": "location"},
    "keelung": {"id": "keelung_port", "type": "location"},
    "yokosuka": {"id": "yokosuka", "type": "location"},
    "guam": {"id": "guam", "type": "location"},
    "bashi channel": {"id": "bashi_channel", "type": "location"},
    "hsinchu": {"id": "hsinchu", "type": "location"},
    "uss ronald reagan": {"id": "uss_reagan", "type": "asset"},
    "uss reagan": {"id": "uss_reagan", "type": "asset"},
    "uss mustin": {"id": "uss_mustin", "type": "asset"},
    "c.c. wei": {"id": "cc_wei", "type": "person"},
    "paparo": {"id": "adm_paparo", "type": "person"},
    "joint sword": {"id": "pla_exercise_2026", "type": "event"},
    "blockade": {"id": "strait_blockade", "type": "threat"},
    "cyber attack": {"id": "cyber_supply_chain", "type": "threat"},
}


class OSINTAgent:
    """Open-source intelligence collection agent.

    Searches the web for relevant intelligence, extracts structured entities,
    and updates the ontology store with new findings and relationships.
    """

    def __init__(self, ontology_store: Optional[OntologyStore] = None, llm: Any = None):
        self.store = ontology_store
        self.llm = llm

    def run(self, query: str, max_results: int = 5) -> OSINTResult:
        """Execute OSINT collection for a given query.

        Args:
            query: Intelligence collection query.
            max_results: Maximum search results to retrieve.

        Returns:
            OSINTResult with findings, extracted entities, and relationships.
        """
        result = OSINTResult(query=query)

        # Step 1: Web search
        search_queries = self._generate_search_queries(query)
        all_search_results: list[SearchResult] = []

        for sq in search_queries:
            results = search_web(sq, max_results=max_results)
            all_search_results.extend(results)

        # Deduplicate by URL
        seen_urls: set[str] = set()
        unique_results: list[SearchResult] = []
        for sr in all_search_results:
            if sr.url not in seen_urls:
                seen_urls.add(sr.url)
                unique_results.append(sr)

        result.search_results = [
            {"title": sr.title, "url": sr.url, "content": sr.content[:500],
             "score": sr.score, "published_date": sr.published_date}
            for sr in unique_results
        ]
        result.sources_consulted = len(unique_results)

        # Step 2: Entity extraction
        extracted = self._extract_entities(unique_results)
        result.extracted_entities = extracted

        # Step 3: Key findings extraction
        result.key_findings = self._extract_key_findings(unique_results)

        # Step 4: Relationship inference
        result.new_relationships = self._infer_relationships(unique_results)

        # Step 5: Update ontology store if available
        if self.store:
            self._update_ontology(result)

        return result

    def _generate_search_queries(self, query: str) -> list[str]:
        """Generate multiple search queries from the input query."""
        queries = [query]
        lower = query.lower()

        if "taiwan" in lower or "strait" in lower:
            queries.append("taiwan strait military exercises 2026")
            queries.append("semiconductor supply chain disruption")
        if "supply chain" in lower:
            queries.append("TSMC production delays shipping")
        if "military" in lower or "defense" in lower:
            queries.append("us military western pacific deployment")

        return queries[:3]  # Limit to 3 queries

    def _extract_entities(self, results: list[SearchResult]) -> list[dict[str, Any]]:
        """Extract structured entities from search results using pattern matching."""
        found_entities: dict[str, dict[str, Any]] = {}

        for sr in results:
            text = (sr.title + " " + sr.content).lower()
            for pattern, entity_info in ENTITY_PATTERNS.items():
                if pattern in text:
                    eid = entity_info["id"]
                    if eid not in found_entities:
                        # Look up from store if available
                        name = eid
                        if self.store:
                            entity = self.store.get_entity(eid)
                            if entity:
                                name = entity.name
                        found_entities[eid] = {
                            "id": eid,
                            "name": name,
                            "type": entity_info["type"],
                            "mentioned_in": [sr.url],
                            "mention_count": 1,
                        }
                    else:
                        found_entities[eid]["mention_count"] += 1
                        if sr.url not in found_entities[eid]["mentioned_in"]:
                            found_entities[eid]["mentioned_in"].append(sr.url)

        return list(found_entities.values())

    def _extract_key_findings(self, results: list[SearchResult]) -> list[str]:
        """Extract key findings from search results."""
        findings: list[str] = []
        for sr in results:
            if sr.score >= 0.85:
                # Take first sentence as a finding
                content = sr.content.strip()
                first_sentence = content.split(". ")[0] + "."
                if len(first_sentence) > 20:
                    findings.append(first_sentence)

        return findings[:8]

    def _infer_relationships(self, results: list[SearchResult]) -> list[dict[str, Any]]:
        """Infer relationships between entities mentioned in the same context."""
        relationships: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()

        for sr in results:
            text = (sr.title + " " + sr.content).lower()
            entities_in_result = []
            for pattern, info in ENTITY_PATTERNS.items():
                if pattern in text:
                    entities_in_result.append(info["id"])

            # Create RELATED_TO relationships for co-occurring entities
            for i, e1 in enumerate(entities_in_result):
                for e2 in entities_in_result[i + 1:]:
                    pair = tuple(sorted([e1, e2]))
                    if pair not in seen:
                        seen.add(pair)
                        relationships.append({
                            "source": e1,
                            "target": e2,
                            "type": "RELATED_TO",
                            "source_url": sr.url,
                            "confidence": sr.score * 0.8,
                        })

        return relationships

    def _update_ontology(self, result: OSINTResult) -> None:
        """Update the ontology store with OSINT findings."""
        for finding in result.key_findings:
            # Add findings as events
            event = Entity(
                name=finding[:80],
                entity_type=EntityType.EVENT,
                description=finding,
                source="osint_agent",
                confidence=0.7,
                tags=["osint_extracted"],
            )
            # Only add if not a duplicate
            existing = self.store.search(finding[:30])
            if not existing:
                self.store.add_entity(event)
