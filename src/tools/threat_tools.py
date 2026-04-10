"""Threat database tools for the Threat Assessor agent.

SCAFFOLDED: Returns realistic mock threat data for demo purposes.
In production, this would connect to classified threat intelligence feeds,
MITRE ATT&CK mappings, and historical incident databases.

Integration points:
- Replace get_threat_intelligence() with real threat feed API (e.g., Recorded Future, Mandiant)
- Replace get_historical_precedents() with historical conflict database
- Add classification markings to all outputs
- Connect to Palantir Gotham for cross-referencing with existing intelligence products
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ThreatIntelligence:
    """Mock threat intelligence item."""
    threat_id: str = ""
    category: str = ""
    severity: str = ""
    confidence: float = 0.0
    description: str = ""
    indicators: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    ttps: list[str] = field(default_factory=list)  # MITRE ATT&CK TTPs


MOCK_THREAT_INTEL: list[dict[str, Any]] = [
    {
        "threat_id": "TI-2026-0451",
        "category": "military_buildup",
        "severity": "critical",
        "confidence": 0.87,
        "description": "PLA Eastern Theater Command has surged naval and air assets to positions consistent with a rehearsal for maritime blockade operations around Taiwan. Satellite imagery confirms deployment of DF-21D anti-ship ballistic missiles to coastal positions.",
        "indicators": ["Increased naval sortie rate", "ASBM transporter-erector-launchers at coastal sites",
                       "Electronic warfare emissions detected", "Civilian maritime traffic advisories issued by PLA"],
        "sources": ["SIGINT", "IMINT", "OSINT"],
        "ttps": ["T1595 - Active Scanning", "T1590 - Gather Victim Network Information"],
    },
    {
        "threat_id": "TI-2026-0452",
        "category": "cyber_operations",
        "severity": "high",
        "confidence": 0.78,
        "description": "APT41 campaign targeting Taiwan critical infrastructure. Confirmed intrusions into port management systems at Kaohsiung and Keelung. Pre-positioned access for potential destructive operations.",
        "indicators": ["ShadowPad malware variants", "C2 infrastructure in SEA",
                       "Spear-phishing targeting port administrators", "Lateral movement in SCADA networks"],
        "sources": ["SIGINT", "Cyber Threat Intelligence", "Partner sharing"],
        "ttps": ["T1566 - Phishing", "T1059 - Command and Scripting Interpreter", "T1078 - Valid Accounts"],
    },
    {
        "threat_id": "TI-2026-0453",
        "category": "economic_coercion",
        "severity": "medium",
        "confidence": 0.72,
        "description": "Coordinated economic pressure campaign including rare earth export restrictions, selective import bans on Taiwanese goods, and diplomatic pressure on ASML export licenses.",
        "indicators": ["Rare earth export quotas tightened", "Customs delays for Taiwanese goods",
                       "Diplomatic demarches to Netherlands", "State media economic warfare narratives"],
        "sources": ["OSINT", "Diplomatic reporting", "Economic intelligence"],
        "ttps": [],
    },
    {
        "threat_id": "TI-2026-0454",
        "category": "gray_zone_operations",
        "severity": "high",
        "confidence": 0.83,
        "description": "PLA-affiliated maritime militia and Chinese Coast Guard vessels conducting harassment operations against commercial shipping in Taiwan Strait. Intentional close approaches to Taiwanese and allied commercial vessels.",
        "indicators": ["Maritime militia fleet mobilization", "CCG patrols in Taiwan EEZ",
                       "AIS spoofing incidents", "Close approach incidents up 400%"],
        "sources": ["Maritime surveillance", "AIS data", "Commercial shipping reports"],
        "ttps": [],
    },
]

MOCK_PRECEDENTS: list[dict[str, Any]] = [
    {
        "event": "1995-1996 Taiwan Strait Crisis",
        "description": "PLA conducted missile tests and military exercises; US deployed two carrier strike groups. De-escalation after show of force.",
        "outcome": "Status quo maintained",
        "relevance_score": 0.85,
    },
    {
        "event": "2022 Pelosi Visit Crisis",
        "description": "PLA conducted unprecedented exercises around Taiwan including missiles over the island. Shipping disrupted for 1 week.",
        "outcome": "Gradual de-escalation, new normal of increased PLA activity",
        "relevance_score": 0.92,
    },
    {
        "event": "2021 Suez Canal Blockage (Ever Given)",
        "description": "Single vessel blockage caused $9.6B/day in trade disruption. Demonstrated fragility of maritime chokepoints.",
        "outcome": "Supply chain diversification push",
        "relevance_score": 0.68,
    },
]


def get_threat_intelligence(region: str = "taiwan_strait") -> list[ThreatIntelligence]:
    """Retrieve threat intelligence for a region.

    SCAFFOLDED: Returns mock data. In production, would query:
    - Classified threat intelligence databases
    - MITRE ATT&CK framework mappings
    - Partner nation intelligence sharing feeds
    - Real-time SIGINT/IMINT analysis products

    Args:
        region: Geographic region identifier.

    Returns:
        List of ThreatIntelligence objects.
    """
    return [ThreatIntelligence(**item) for item in MOCK_THREAT_INTEL]


def get_historical_precedents(scenario_type: str = "strait_crisis") -> list[dict[str, Any]]:
    """Retrieve historical precedents for scenario analysis.

    SCAFFOLDED: Returns mock historical data. In production, would query:
    - Classified historical incident database
    - Academic conflict databases (COW, UCDP)
    - Previous intelligence assessments

    Args:
        scenario_type: Type of scenario for precedent matching.

    Returns:
        List of historical precedent dictionaries.
    """
    return MOCK_PRECEDENTS


def calculate_risk_matrix(threat_intel: list[ThreatIntelligence]) -> dict[str, Any]:
    """Calculate aggregate risk matrix from threat intelligence.

    Args:
        threat_intel: List of threat intelligence items.

    Returns:
        Risk matrix with overall score and category breakdowns.
    """
    severity_weights = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
    category_scores: dict[str, float] = {}

    for ti in threat_intel:
        weight = severity_weights.get(ti.severity, 0.5)
        score = weight * ti.confidence
        category_scores[ti.category] = max(category_scores.get(ti.category, 0), score)

    overall = sum(category_scores.values()) / max(len(category_scores), 1)

    return {
        "overall_risk_score": round(overall, 2),
        "category_scores": category_scores,
        "threat_count": len(threat_intel),
        "highest_severity": max((ti.severity for ti in threat_intel), default="unknown",
                                key=lambda s: severity_weights.get(s, 0)),
    }
