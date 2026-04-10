"""Briefing document generation tools.

SCAFFOLDED: Template-based briefing generation for demo purposes.
In production, this would integrate with:
- Palantir document generation pipeline
- Classification marking system (FOUO, SECRET, TS/SCI)
- Automated distribution lists
- Version control and audit logging
- Multi-format output (PDF, DOCX, HTML, Palantir Report)
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional


BRIEFING_TEMPLATE = """
================================================================================
                    EXECUTIVE INTELLIGENCE BRIEFING
                    {classification}
================================================================================
DATE:     {date}
SUBJECT:  {subject}
ANALYST:  Multi-Agent Intelligence System (Automated)
SOURCES:  {source_count} OSINT sources, Ontology Graph Analysis, Threat Intelligence
================================================================================

1. EXECUTIVE SUMMARY
--------------------
{executive_summary}

2. KEY FINDINGS
---------------
{key_findings}

3. ONTOLOGY ANALYSIS
--------------------
{ontology_analysis}

4. RISK ASSESSMENT
------------------
{risk_assessment}

5. SUPPLY CHAIN IMPACT
----------------------
{supply_chain_impact}

6. MILITARY POSTURE
-------------------
{military_posture}

7. RECOMMENDATIONS
------------------
{recommendations}

8. OUTLOOK
----------
{outlook}

================================================================================
CLASSIFICATION: {classification}
DISTRIBUTION: {distribution}
NEXT UPDATE:  {next_update}
================================================================================
"""


def generate_briefing_document(
    subject: str,
    executive_summary: str,
    key_findings: str,
    ontology_analysis: str = "See attached ontology graph visualization.",
    risk_assessment: str = "Risk assessment pending.",
    supply_chain_impact: str = "Supply chain analysis pending.",
    military_posture: str = "Military posture analysis pending.",
    recommendations: str = "Recommendations pending full analysis.",
    outlook: str = "Outlook assessment pending.",
    classification: str = "UNCLASSIFIED // FOR OFFICIAL USE ONLY",
    distribution: Optional[str] = None,
) -> str:
    """Generate a formatted executive briefing document.

    SCAFFOLDED: Uses text template. In production, would:
    - Apply proper classification markings per IC standards
    - Generate PDF with digital signatures
    - Route through Palantir document management
    - Include interactive ontology graph embeds
    - Support multiple classification levels

    Args:
        subject: Briefing subject line.
        executive_summary: 2-3 paragraph executive summary.
        key_findings: Bullet-pointed key findings.
        ontology_analysis: Ontology graph analysis summary.
        risk_assessment: Threat and risk assessment section.
        supply_chain_impact: Supply chain disruption analysis.
        military_posture: Military force posture summary.
        recommendations: Actionable recommendations.
        outlook: Forward-looking assessment.
        classification: Classification marking.
        distribution: Distribution list.

    Returns:
        Formatted briefing document string.
    """
    if distribution is None:
        distribution = "SECDEF, NSC, INDOPACOM, USTR"

    return BRIEFING_TEMPLATE.format(
        date=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        subject=subject,
        classification=classification,
        source_count="Multiple",
        executive_summary=executive_summary,
        key_findings=key_findings,
        ontology_analysis=ontology_analysis,
        risk_assessment=risk_assessment,
        supply_chain_impact=supply_chain_impact,
        military_posture=military_posture,
        recommendations=recommendations,
        outlook=outlook,
        distribution=distribution,
        next_update=(datetime.utcnow().strftime("%Y-%m-%d") + " + 24h"),
    )


def format_findings_as_bullets(findings: list[dict[str, Any]]) -> str:
    """Format a list of finding dicts into bullet points.

    Args:
        findings: List of dicts with 'title' and 'detail' keys.

    Returns:
        Formatted bullet point string.
    """
    lines = []
    for i, finding in enumerate(findings, 1):
        title = finding.get("title", f"Finding {i}")
        detail = finding.get("detail", "")
        lines.append(f"  {i}. {title}")
        if detail:
            lines.append(f"     {detail}")
        lines.append("")
    return "\n".join(lines)


def format_risk_table(risk_data: dict[str, Any]) -> str:
    """Format risk assessment data into a text table.

    Args:
        risk_data: Risk assessment dictionary.

    Returns:
        Formatted text table.
    """
    lines = [
        f"  Overall Risk Score: {risk_data.get('overall_risk_score', 'N/A')}",
        f"  Highest Severity:   {risk_data.get('highest_severity', 'N/A')}",
        "",
        "  Category Breakdown:",
    ]
    for category, score in risk_data.get("category_scores", {}).items():
        bar = "#" * int(score * 20)
        lines.append(f"    {category:<25s} [{bar:<20s}] {score:.2f}")

    return "\n".join(lines)
