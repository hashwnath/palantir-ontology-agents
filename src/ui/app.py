"""Streamlit demo UI for the multi-agent ontology workflow.

Provides:
- Query input with "Run Analysis" button
- Agent activity timeline in sidebar
- Ontology graph visualization
- Result panels for each agent
- Final briefing display
"""

from __future__ import annotations

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st

from src.orchestrator import Orchestrator
from src.ontology.loader import load_sample_data


# --- Page config ---
st.set_page_config(
    page_title="Palantir Ontology Agents",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_header():
    st.title("Multi-Agent Ontology Workflow")
    st.caption("AIP-style agentic intelligence analysis with LangGraph")
    st.markdown("---")


def render_ontology_graph():
    """Render the ontology graph visualization using graphviz."""
    store = load_sample_data()

    dot_lines = [
        "digraph ontology {",
        '  rankdir=LR;',
        '  node [shape=box, style=filled, fontsize=10];',
        '  edge [fontsize=8];',
    ]

    # Color map by entity type
    colors = {
        "organization": "#90EE90",
        "person": "#87CEEB",
        "location": "#FFB6C1",
        "event": "#FFD700",
        "asset": "#DDA0DD",
        "threat": "#FF6347",
    }

    # Add nodes
    for entity in store.all_entities():
        color = colors.get(entity.entity_type.value, "#FFFFFF")
        label = entity.name.replace('"', '\\"')
        if len(label) > 25:
            label = label[:22] + "..."
        dot_lines.append(
            f'  "{entity.id}" [label="{label}", fillcolor="{color}"];'
        )

    # Add edges (limit to key relationships for readability)
    rel_count = 0
    for rel in store.all_relationships():
        if rel_count > 60:
            break
        label = rel.relationship_type.value.replace("_", " ")
        dot_lines.append(
            f'  "{rel.source_id}" -> "{rel.target_id}" [label="{label}"];'
        )
        rel_count += 1

    dot_lines.append("}")
    return "\n".join(dot_lines)


def render_sidebar_timeline(timeline: list[dict]):
    """Render agent activity timeline in the sidebar."""
    st.sidebar.markdown("## Agent Activity")

    status_icons = {
        "started": "⏳",
        "completed": "✅",
        "error": "❌",
    }

    agent_colors = {
        "coordinator": "🔵",
        "osint_collector": "🟢",
        "graph_analyst": "🟢",
        "threat_assessor": "🟡",
        "briefing_drafter": "🟡",
    }

    for entry in timeline:
        icon = status_icons.get(entry.get("status", ""), "⬜")
        agent_icon = agent_colors.get(entry.get("agent", ""), "⬜")
        agent = entry.get("agent", "unknown").replace("_", " ").title()
        detail = entry.get("detail", "")
        timestamp = entry.get("timestamp", "")[:19]

        st.sidebar.markdown(
            f"{agent_icon} **{agent}** {icon}\n\n"
            f"  {detail}\n\n"
            f"  `{timestamp}`"
        )
        st.sidebar.markdown("---")


def render_osint_panel(osint_results: dict):
    """Render OSINT results panel."""
    st.subheader("OSINT Collection")

    if not osint_results:
        st.info("Awaiting OSINT results...")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sources Consulted", osint_results.get("sources_consulted", 0))
    with col2:
        st.metric("Entities Extracted", len(osint_results.get("extracted_entities", [])))

    # Key findings
    findings = osint_results.get("key_findings", [])
    if findings:
        st.markdown("**Key Findings:**")
        for f in findings:
            st.markdown(f"- {f}")

    # Search results
    with st.expander("Search Results", expanded=False):
        for sr in osint_results.get("search_results", []):
            st.markdown(f"**[{sr.get('title', '')}]({sr.get('url', '')})**")
            st.caption(sr.get("content", "")[:200])
            st.markdown("---")

    # Extracted entities
    with st.expander("Extracted Entities", expanded=False):
        for entity in osint_results.get("extracted_entities", []):
            st.markdown(f"- **{entity.get('name', '')}** ({entity.get('type', '')}) - "
                        f"mentioned {entity.get('mention_count', 0)} times")


def render_graph_panel(graph_results: dict):
    """Render Graph Analysis results panel."""
    st.subheader("Graph Analysis")

    if not graph_results:
        st.info("Awaiting graph analysis...")
        return

    exposure_scores = graph_results.get("exposure_scores", [])
    hub_entities = graph_results.get("hub_entities", [])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Entities Analyzed", len(exposure_scores))
    with col2:
        high_exp = sum(1 for e in exposure_scores if e.get("exposure_score", 0) >= 0.6)
        st.metric("High Exposure Entities", high_exp)

    # Key findings
    findings = graph_results.get("key_findings", [])
    if findings:
        st.markdown("**Key Findings:**")
        for f in findings:
            st.markdown(f"- {f}")

    # Exposure scores
    with st.expander("Exposure Scores", expanded=False):
        for entry in exposure_scores:
            if entry.get("exposure_score", 0) > 0:
                score = entry["exposure_score"]
                bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
                st.text(f"{entry['name']:<30s} [{bar}] {score:.2f}")

    # Hub entities
    with st.expander("Hub Entities", expanded=False):
        for hub in hub_entities:
            st.markdown(f"- **{hub['name']}** ({hub['type']}) - {hub['degree']} connections")


def render_threat_panel(threat_results: dict):
    """Render Threat Assessment results panel."""
    st.subheader("Threat Assessment")

    if not threat_results:
        st.info("Awaiting threat assessment...")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        risk_level = threat_results.get("overall_risk_level", "UNKNOWN")
        color = {"CRITICAL": "🔴", "HIGH": "🟠", "ELEVATED": "🟡", "GUARDED": "🟢", "LOW": "🟢"}.get(risk_level, "⚪")
        st.metric("Risk Level", f"{color} {risk_level}")
    with col2:
        st.metric("Risk Score", f"{threat_results.get('overall_risk_score', 0):.2f}")
    with col3:
        st.metric("Confidence", f"{threat_results.get('confidence', 0):.2f}")

    # Key findings
    findings = threat_results.get("key_findings", [])
    if findings:
        st.markdown("**Key Findings:**")
        for f in findings:
            st.markdown(f"- {f}")

    # Threat details
    with st.expander("Threat Assessments", expanded=False):
        for ta in threat_results.get("threat_assessments", []):
            severity_color = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(ta.get("severity", ""), "⚪")
            st.markdown(f"**{severity_color} {ta.get('category', '').replace('_', ' ').title()}** "
                        f"(Severity: {ta.get('severity', '')}, Confidence: {ta.get('confidence', 0):.2f})")
            st.caption(ta.get("description", ""))
            st.markdown("---")


def render_briefing_panel(briefing: dict):
    """Render the final executive briefing."""
    st.subheader("Executive Briefing")

    if not briefing:
        st.info("Awaiting briefing generation...")
        return

    metadata = briefing.get("metadata", {})
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("OSINT Sources", metadata.get("osint_sources", 0))
    with col2:
        st.metric("Entities Analyzed", metadata.get("entities_analyzed", 0))
    with col3:
        st.metric("Threat Level", metadata.get("threat_level", "N/A"))

    # Full briefing text
    briefing_text = briefing.get("briefing_text", "")
    if briefing_text:
        st.code(briefing_text, language=None)


def main():
    render_header()

    # Sidebar
    st.sidebar.title("Control Panel")

    # Default demo query
    default_query = (
        "Track all supply chain disruptions in the Taiwan Strait region, "
        "cross-reference with our partner network exposure, assess military "
        "readiness implications, and draft an executive briefing for the SECDEF meeting at 0800."
    )

    query = st.text_area("Intelligence Query", value=default_query, height=100)

    col1, col2 = st.columns([1, 3])
    with col1:
        run_button = st.button("Run Analysis", type="primary", use_container_width=True)
    with col2:
        show_graph = st.checkbox("Show Ontology Graph", value=False)

    # Ontology graph visualization
    if show_graph:
        st.markdown("### Ontology Graph")
        with st.spinner("Rendering ontology graph..."):
            dot_source = render_ontology_graph()
            st.graphviz_chart(dot_source, use_container_width=True)

    st.markdown("---")

    # Run the workflow
    if run_button:
        orchestrator = Orchestrator()
        timeline: list[dict] = []

        # Create placeholders for streaming updates
        status_placeholder = st.empty()
        progress_bar = st.progress(0)

        agent_steps = [
            ("coordinator", 0.15),
            ("osint_collector", 0.35),
            ("graph_analyst", 0.55),
            ("threat_assessor", 0.75),
            ("briefing_drafter", 1.0),
        ]

        step_idx = 0
        full_state: dict = {}

        status_placeholder.info("Starting multi-agent workflow...")

        try:
            for node_name, state_update in orchestrator.run_stream(query):
                full_state.update(state_update)

                # Update timeline
                if "timeline" in state_update:
                    timeline = state_update["timeline"]

                # Update progress
                for i, (name, progress) in enumerate(agent_steps):
                    if name == node_name:
                        step_idx = i
                        break
                progress_val = agent_steps[min(step_idx, len(agent_steps) - 1)][1]
                progress_bar.progress(progress_val)
                status_placeholder.info(f"Running: {node_name.replace('_', ' ').title()}...")

                # Render sidebar timeline
                render_sidebar_timeline(timeline)

            progress_bar.progress(1.0)
            status_placeholder.success("Analysis complete!")

        except Exception as e:
            status_placeholder.error(f"Workflow error: {e}")
            st.exception(e)
            return

        # Render result panels
        tab1, tab2, tab3, tab4 = st.tabs([
            "OSINT Collection", "Graph Analysis", "Threat Assessment", "Executive Briefing"
        ])

        with tab1:
            render_osint_panel(full_state.get("osint_results", {}))
        with tab2:
            render_graph_panel(full_state.get("graph_results", {}))
        with tab3:
            render_threat_panel(full_state.get("threat_results", {}))
        with tab4:
            render_briefing_panel(full_state.get("briefing", {}))

    else:
        # Show demo ontology stats
        st.markdown("### Demo Scenario: Taiwan Strait Supply Chain Disruption")
        store = load_sample_data()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Entities", store.entity_count)
        with col2:
            st.metric("Relationships", store.relationship_count)
        with col3:
            from src.ontology.schema import EntityType
            st.metric("Organizations", len(store.query_by_type(EntityType.ORGANIZATION)))
        with col4:
            st.metric("Threats", len(store.query_by_type(EntityType.THREAT)))

        st.info("Click **Run Analysis** to start the multi-agent intelligence workflow.")

        # Architecture diagram
        st.markdown("### Workflow Architecture")
        arch_dot = """
        digraph workflow {
            rankdir=LR;
            node [shape=box, style=filled, fontsize=11];

            start [label="User Query", shape=ellipse, fillcolor="#E8E8E8"];
            coord [label="Coordinator", fillcolor="#90EE90"];
            osint [label="OSINT Collector", fillcolor="#90EE90"];
            graph [label="Graph Analyst", fillcolor="#90EE90"];
            threat [label="Threat Assessor", fillcolor="#FFD700"];
            brief [label="Briefing Drafter", fillcolor="#FFD700"];
            out [label="Executive Briefing", shape=ellipse, fillcolor="#E8E8E8"];
            ont [label="Ontology Store", shape=cylinder, fillcolor="#90EE90"];

            start -> coord;
            coord -> osint;
            coord -> graph;
            osint -> ont [style=dashed, label="update"];
            graph -> ont [style=dashed, label="traverse"];
            osint -> threat;
            graph -> threat;
            threat -> brief;
            brief -> out;
        }
        """
        st.graphviz_chart(arch_dot, use_container_width=True)


if __name__ == "__main__":
    main()
