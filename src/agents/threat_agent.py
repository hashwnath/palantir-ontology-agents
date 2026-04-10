"""Threat Assessor Agent - Risk scoring and threat assessment.

SCAFFOLDED: Uses mock threat intelligence data for demo purposes.
In production, this agent would:
- Query classified threat intelligence databases (e.g., Palantir Gotham threat feeds)
- Cross-reference OSINT findings with SIGINT/IMINT/HUMINT sources
- Apply ML-based threat scoring models trained on historical conflict data
- Generate MITRE ATT&CK mappings for cyber threats
- Produce assessments with proper IC confidence language (likely, highly likely, etc.)
- Apply classification markings based on source material

Integration points:
- ThreatIntelligenceAPI: Replace mock data with real threat feed connector
- HistoricalAnalysisEngine: Replace mock precedents with ML-powered precedent matching
- ClassificationEngine: Add automatic classification marking based on sources used
- ConfidenceCalibration: Add calibrated confidence scoring model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from src.agents.osint_agent import OSINTResult
from src.agents.graph_agent import GraphAnalysisResult
from src.tools.threat_tools import (
    ThreatIntelligence,
    get_threat_intelligence,
    get_historical_precedents,
    calculate_risk_matrix,
)


@dataclass
class ThreatAssessmentResult:
    """Result from threat assessment run."""
    query: str = ""
    overall_risk_score: float = 0.0
    overall_risk_level: str = "unknown"
    confidence: float = 0.0
    threat_assessments: list[dict[str, Any]] = field(default_factory=list)
    risk_matrix: dict[str, Any] = field(default_factory=dict)
    historical_precedents: list[dict[str, Any]] = field(default_factory=list)
    escalation_indicators: list[str] = field(default_factory=list)
    mitigating_factors: list[str] = field(default_factory=list)
    key_findings: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "overall_risk_score": self.overall_risk_score,
            "overall_risk_level": self.overall_risk_level,
            "confidence": self.confidence,
            "threat_assessments": self.threat_assessments,
            "risk_matrix": self.risk_matrix,
            "historical_precedents": self.historical_precedents,
            "escalation_indicators": self.escalation_indicators,
            "mitigating_factors": self.mitigating_factors,
            "key_findings": self.key_findings,
            "timestamp": self.timestamp,
        }


class ThreatAssessorAgent:
    """Threat assessment agent for risk scoring and threat analysis.

    SCAFFOLDED: Produces realistic threat assessments using mock data.
    Demonstrates the assessment structure and integration points that would
    connect to classified intelligence feeds in production.
    """

    def __init__(self, llm: Any = None):
        self.llm = llm

    def run(self, query: str,
            osint_result: Optional[OSINTResult] = None,
            graph_result: Optional[GraphAnalysisResult] = None) -> ThreatAssessmentResult:
        """Execute threat assessment.

        Args:
            query: Assessment query.
            osint_result: Optional OSINT findings to incorporate.
            graph_result: Optional graph analysis to incorporate.

        Returns:
            ThreatAssessmentResult with risk scores and assessments.
        """
        result = ThreatAssessmentResult(query=query)

        # Step 1: Get threat intelligence (mock)
        threat_intel = get_threat_intelligence("taiwan_strait")

        # Step 2: Calculate risk matrix
        result.risk_matrix = calculate_risk_matrix(threat_intel)
        result.overall_risk_score = result.risk_matrix["overall_risk_score"]
        result.overall_risk_level = self._score_to_level(result.overall_risk_score)

        # Step 3: Get historical precedents
        result.historical_precedents = get_historical_precedents("strait_crisis")

        # Step 4: Build individual threat assessments
        for ti in threat_intel:
            assessment = {
                "threat_id": ti.threat_id,
                "category": ti.category,
                "severity": ti.severity,
                "confidence": ti.confidence,
                "description": ti.description,
                "indicators": ti.indicators,
                "assessment": self._assess_individual_threat(ti, osint_result, graph_result),
            }
            result.threat_assessments.append(assessment)

        # Step 5: Aggregate confidence
        confidences = [ti.confidence for ti in threat_intel]
        result.confidence = round(sum(confidences) / max(len(confidences), 1), 2)

        # Step 6: Identify escalation indicators and mitigating factors
        result.escalation_indicators = self._identify_escalation_indicators(threat_intel, osint_result)
        result.mitigating_factors = self._identify_mitigating_factors(threat_intel, graph_result)

        # Step 7: Key findings
        result.key_findings = self._generate_findings(result)

        return result

    def _score_to_level(self, score: float) -> str:
        """Convert numeric risk score to categorical level."""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "ELEVATED"
        elif score >= 0.2:
            return "GUARDED"
        else:
            return "LOW"

    def _assess_individual_threat(self, ti: ThreatIntelligence,
                                   osint_result: Optional[OSINTResult],
                                   graph_result: Optional[GraphAnalysisResult]) -> str:
        """Generate assessment text for an individual threat."""
        assessments = {
            "military_buildup": (
                "PLA force posture is consistent with coercive military signaling, with indicators "
                "suggesting readiness for escalation to blockade operations. Current assessment: "
                "exercises are primarily signaling but maintain real escalation potential."
            ),
            "cyber_operations": (
                "Cyber operations targeting Taiwan critical infrastructure represent a serious "
                "pre-positioning effort. The combination of port system intrusions and SCADA "
                "network access indicates preparation for potential destructive operations "
                "synchronized with kinetic military activity."
            ),
            "economic_coercion": (
                "Economic pressure campaign is coordinated and multi-vector. Export control "
                "pressure on semiconductor equipment supply chain represents long-term strategic "
                "threat to Taiwan's technology advantage. Current impact is moderate but escalation "
                "pathways exist."
            ),
            "gray_zone_operations": (
                "Maritime gray zone operations are designed to normalize PLA presence and erode "
                "freedom of navigation in the Taiwan Strait. The 400% increase in close approach "
                "incidents significantly raises risk of accidental escalation."
            ),
        }
        return assessments.get(ti.category, f"Assessment pending for {ti.category} threat category.")

    def _identify_escalation_indicators(self, threat_intel: list[ThreatIntelligence],
                                         osint_result: Optional[OSINTResult]) -> list[str]:
        """Identify factors that could lead to escalation."""
        indicators = [
            "PLA exercise scale exceeds previous demonstrations (Joint Sword-2026A)",
            "Simultaneous cyber and kinetic preparation indicators",
            "Commercial shipping disruption creating economic pressure on Taiwan",
            "Dual carrier deployment (Liaoning + Shandong) not seen since 2022",
        ]

        if osint_result and osint_result.sources_consulted > 3:
            indicators.append(
                f"Elevated media coverage ({osint_result.sources_consulted} sources) "
                "indicates sustained international attention"
            )

        return indicators

    def _identify_mitigating_factors(self, threat_intel: list[ThreatIntelligence],
                                      graph_result: Optional[GraphAnalysisResult]) -> list[str]:
        """Identify factors that reduce escalation risk."""
        factors = [
            "US carrier strike group deployment provides deterrent signaling",
            "No indicators of PLA mobilization beyond exercise participants",
            "Diplomatic channels remain open (back-channel communications reported)",
            "PLA exercises have defined end date (March 22), suggesting limited scope",
            "Economic interdependence creates mutual costs for sustained disruption",
        ]

        if graph_result and graph_result.exposure_scores:
            high_exposure = sum(1 for e in graph_result.exposure_scores if e["exposure_score"] >= 0.6)
            factors.append(
                f"Graph analysis shows {high_exposure} high-exposure entities, "
                "creating economic disincentive for escalation on both sides"
            )

        return factors

    def _generate_findings(self, result: ThreatAssessmentResult) -> list[str]:
        """Generate key findings from the threat assessment."""
        findings = [
            f"Overall risk level: {result.overall_risk_level} "
            f"(score: {result.overall_risk_score:.2f}, confidence: {result.confidence:.2f})",
        ]

        critical_threats = [ta for ta in result.threat_assessments if ta["severity"] == "critical"]
        if critical_threats:
            findings.append(
                f"{len(critical_threats)} CRITICAL threat(s) identified: "
                + ", ".join(ta["category"] for ta in critical_threats)
            )

        if result.historical_precedents:
            most_relevant = max(result.historical_precedents, key=lambda p: p["relevance_score"])
            findings.append(
                f"Most relevant historical precedent: {most_relevant['event']} "
                f"(relevance: {most_relevant['relevance_score']:.2f})"
            )

        findings.append(
            f"{len(result.escalation_indicators)} escalation indicators vs "
            f"{len(result.mitigating_factors)} mitigating factors identified"
        )

        return findings
