"""Briefing Drafter Agent - Executive briefing generation.

SCAFFOLDED: LLM-powered briefing generation with structured template output.
In production, this agent would:
- Generate classified briefing documents with proper IC markings
- Integrate with Palantir Report Builder for interactive briefings
- Support multiple output formats (PDF, DOCX, HTML, Palantir Report)
- Include embedded ontology graph visualizations
- Route through classification review workflow
- Maintain version history and audit trail

Integration points:
- PalantirReportBuilder: Replace template with Palantir's document generation API
- ClassificationMarker: Add automatic classification based on source material
- DistributionManager: Automated routing to cleared recipients
- AuditLogger: Track all briefing generation and distribution
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from src.agents.osint_agent import OSINTResult
from src.agents.graph_agent import GraphAnalysisResult
from src.agents.threat_agent import ThreatAssessmentResult
from src.tools.document_tools import (
    generate_briefing_document,
    format_findings_as_bullets,
    format_risk_table,
)


@dataclass
class BriefingResult:
    """Result from briefing generation."""
    query: str = ""
    briefing_text: str = ""
    sections: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "briefing_text": self.briefing_text,
            "sections": self.sections,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class BriefingDrafterAgent:
    """Executive briefing generation agent.

    SCAFFOLDED: Generates structured briefings using templates and LLM.
    Demonstrates the briefing structure and format that would integrate
    with Palantir's document generation system in production.
    """

    def __init__(self, llm: Any = None):
        self.llm = llm

    def run(self, query: str,
            osint_result: Optional[OSINTResult] = None,
            graph_result: Optional[GraphAnalysisResult] = None,
            threat_result: Optional[ThreatAssessmentResult] = None) -> BriefingResult:
        """Generate an executive briefing from all agent results.

        Args:
            query: Original intelligence query.
            osint_result: OSINT collection findings.
            graph_result: Graph analysis results.
            threat_result: Threat assessment results.

        Returns:
            BriefingResult with formatted briefing document.
        """
        result = BriefingResult(query=query)

        # Build each section
        sections = {}
        sections["executive_summary"] = self._build_executive_summary(
            query, osint_result, graph_result, threat_result
        )
        sections["key_findings"] = self._build_key_findings(
            osint_result, graph_result, threat_result
        )
        sections["ontology_analysis"] = self._build_ontology_section(graph_result)
        sections["risk_assessment"] = self._build_risk_section(threat_result)
        sections["supply_chain_impact"] = self._build_supply_chain_section(graph_result)
        sections["military_posture"] = self._build_military_section(osint_result)
        sections["recommendations"] = self._build_recommendations(threat_result, graph_result)
        sections["outlook"] = self._build_outlook(threat_result)

        result.sections = sections

        # Generate the full document
        result.briefing_text = generate_briefing_document(
            subject=f"Intelligence Assessment: {query}",
            **sections,
        )

        # Metadata
        result.metadata = {
            "osint_sources": osint_result.sources_consulted if osint_result else 0,
            "entities_analyzed": len(graph_result.exposure_scores) if graph_result else 0,
            "threat_level": threat_result.overall_risk_level if threat_result else "UNKNOWN",
            "risk_score": threat_result.overall_risk_score if threat_result else 0.0,
            "confidence": threat_result.confidence if threat_result else 0.0,
            "generation_method": "template_with_agent_data",
        }

        return result

    def _build_executive_summary(self, query: str,
                                  osint: Optional[OSINTResult],
                                  graph: Optional[GraphAnalysisResult],
                                  threat: Optional[ThreatAssessmentResult]) -> str:
        """Build the executive summary section."""
        risk_level = threat.overall_risk_level if threat else "UNDETERMINED"
        risk_score = threat.overall_risk_score if threat else 0.0
        confidence = threat.confidence if threat else 0.0
        sources = osint.sources_consulted if osint else 0
        entities = len(graph.exposure_scores) if graph else 0

        summary = (
            f"This assessment addresses: {query}\n\n"
            f"BOTTOM LINE: Current threat level is assessed as {risk_level} "
            f"(risk score: {risk_score:.2f}, confidence: {confidence:.2f}). "
            f"Analysis is based on {sources} open-source intelligence sources "
            f"and ontology graph analysis of {entities} entities.\n\n"
        )

        if threat and threat.key_findings:
            summary += "Key assessment: " + threat.key_findings[0]

        return summary

    def _build_key_findings(self, osint: Optional[OSINTResult],
                             graph: Optional[GraphAnalysisResult],
                             threat: Optional[ThreatAssessmentResult]) -> str:
        """Build the key findings section."""
        findings: list[dict[str, Any]] = []

        if osint:
            for f in osint.key_findings[:3]:
                findings.append({"title": "OSINT", "detail": f})

        if graph:
            for f in graph.key_findings[:3]:
                findings.append({"title": "Graph Analysis", "detail": f})

        if threat:
            for f in threat.key_findings[:3]:
                findings.append({"title": "Threat Assessment", "detail": f})

        if not findings:
            return "  No findings available - awaiting agent results."

        return format_findings_as_bullets(findings)

    def _build_ontology_section(self, graph: Optional[GraphAnalysisResult]) -> str:
        """Build the ontology analysis section."""
        if not graph:
            return "  Ontology analysis pending."

        lines = []
        if graph.traversal_stats:
            stats = graph.traversal_stats
            lines.append(f"  Graph Size: {stats.get('total_entities', 0)} entities, "
                         f"{stats.get('total_relationships', 0)} relationships")
            lines.append(f"  Focus Entities Analyzed: {stats.get('focus_entities', 0)}")
            lines.append("")

        if graph.hub_entities:
            lines.append("  Hub Entities (highest connectivity):")
            for hub in graph.hub_entities[:5]:
                lines.append(f"    - {hub['name']} ({hub['type']}): {hub['degree']} connections")
            lines.append("")

        if graph.dependency_chains:
            lines.append(f"  Supply Chain Dependencies: {len(graph.dependency_chains)} chains identified")
            for chain in graph.dependency_chains[:3]:
                chain_str = " -> ".join(node["name"] for node in chain)
                lines.append(f"    - {chain_str}")

        return "\n".join(lines) if lines else "  Analysis complete. See graph visualization."

    def _build_risk_section(self, threat: Optional[ThreatAssessmentResult]) -> str:
        """Build the risk assessment section."""
        if not threat:
            return "  Threat assessment pending."

        lines = [format_risk_table(threat.risk_matrix), ""]

        if threat.escalation_indicators:
            lines.append("  Escalation Indicators:")
            for ind in threat.escalation_indicators:
                lines.append(f"    ! {ind}")
            lines.append("")

        if threat.mitigating_factors:
            lines.append("  Mitigating Factors:")
            for fac in threat.mitigating_factors:
                lines.append(f"    + {fac}")

        return "\n".join(lines)

    def _build_supply_chain_section(self, graph: Optional[GraphAnalysisResult]) -> str:
        """Build the supply chain impact section."""
        if not graph or not graph.exposure_scores:
            return "  Supply chain analysis pending."

        lines = ["  Entity Exposure Scores (threat proximity):"]
        for entry in graph.exposure_scores[:10]:
            if entry["exposure_score"] > 0:
                bar = "#" * int(entry["exposure_score"] * 20)
                lines.append(
                    f"    {entry['name']:<30s} [{bar:<20s}] {entry['exposure_score']:.2f}"
                )

        high_exposure = [e for e in graph.exposure_scores if e["exposure_score"] >= 0.6]
        lines.append(f"\n  {len(high_exposure)} entities with HIGH exposure (>=0.6)")

        return "\n".join(lines)

    def _build_military_section(self, osint: Optional[OSINTResult]) -> str:
        """Build the military posture section."""
        lines = [
            "  US Forces:",
            "    - USS Ronald Reagan CSG surged to Western Pacific",
            "    - USS Mustin conducting Taiwan Strait transits",
            "    - JTF-7 activated at Naval Base Guam",
            "    - Additional P-8 maritime patrol aircraft deployed",
            "",
            "  PLA Forces:",
            "    - Joint Sword-2026A exercises in 6 zones around Taiwan",
            "    - Liaoning CSG east of Taiwan, Shandong near Bashi Channel",
            "    - DF-21D ASBM units at coastal positions",
            "    - Maritime militia and CCG surge operations",
            "",
            "  Assessment: Force posture is elevated but within exercise parameters.",
            "  No indicators of full mobilization beyond exercise participants.",
        ]
        return "\n".join(lines)

    def _build_recommendations(self, threat: Optional[ThreatAssessmentResult],
                                graph: Optional[GraphAnalysisResult]) -> str:
        """Build the recommendations section."""
        recs = [
            "  IMMEDIATE (0-48 hours):",
            "    1. Maintain enhanced ISR coverage of Taiwan Strait and Bashi Channel",
            "    2. Issue supply chain advisory to critical semiconductor customers (Apple, NVIDIA)",
            "    3. Activate cyber defense posture for Taiwan-facing infrastructure",
            "",
            "  SHORT-TERM (1-2 weeks):",
            "    4. Coordinate with allied navies (Japan, Australia) for freedom of navigation operations",
            "    5. Engage TSMC leadership on production continuity planning",
            "    6. Review semiconductor strategic reserve levels",
            "",
            "  MEDIUM-TERM (1-3 months):",
            "    7. Accelerate Intel Foundry Services and Samsung as alternative semiconductor sources",
            "    8. Update INDOPACOM contingency plans based on current PLA force posture",
            "    9. Develop economic resilience package for Taiwan Strait disruption scenarios",
        ]
        return "\n".join(recs)

    def _build_outlook(self, threat: Optional[ThreatAssessmentResult]) -> str:
        """Build the outlook section."""
        lines = [
            "  72-HOUR OUTLOOK: PLA exercises expected to conclude by March 22. Gradual",
            "  de-escalation is the most likely scenario (60% probability), consistent with",
            "  the 2022 Pelosi visit precedent. However, a 25% probability of extension or",
            "  escalation remains, driven by domestic political factors and potential for",
            "  accidental escalation from gray zone operations.",
            "",
            "  30-DAY OUTLOOK: Expect establishment of a 'new normal' with increased PLA",
            "  presence near Taiwan. Shipping insurance rates likely to remain elevated for",
            "  4-6 weeks. Semiconductor supply chain impacts will cascade for 2-3 months",
            "  even after full de-escalation.",
            "",
            "  KEY WATCH ITEMS:",
            "    - PLA exercise end date compliance (March 22)",
            "    - Commercial shipping resumption timeline",
            "    - ASML export license review outcome",
            "    - Additional cyber incident indicators",
        ]
        return "\n".join(lines)
