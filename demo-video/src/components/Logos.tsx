import { COLORS } from "../theme";

interface MarkProps {
  size?: number;
}

// Palantir mark - geometric eye/seeing-stone motif
export const PalantirMark: React.FC<MarkProps> = ({ size = 28 }) => (
  <svg width={size} height={size} viewBox="0 0 28 28">
    <circle cx="14" cy="14" r="12" stroke={COLORS.palantirMark} strokeWidth="1.5" fill="none" opacity={0.3} />
    <circle cx="14" cy="14" r="8" stroke={COLORS.palantirMark} strokeWidth="1" fill="none" opacity={0.5} />
    <circle cx="14" cy="14" r="4" fill={COLORS.palantirMark} opacity={0.9} />
    <line x1="2" y1="14" x2="26" y2="14" stroke={COLORS.palantirMark} strokeWidth="0.5" opacity={0.2} />
    <line x1="14" y1="2" x2="14" y2="26" stroke={COLORS.palantirMark} strokeWidth="0.5" opacity={0.2} />
  </svg>
);

// OSINT agent - radar/search sweep
export const OSINTMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="9" stroke={COLORS.osint} strokeWidth="1.5" fill="none" opacity={0.3} />
    <circle cx="12" cy="12" r="5" stroke={COLORS.osint} strokeWidth="1.5" fill="none" opacity={0.5} />
    <circle cx="12" cy="12" r="2" fill={COLORS.osint} />
    <line x1="12" y1="12" x2="19" y2="5" stroke={COLORS.osint} strokeWidth="2" strokeLinecap="round" />
  </svg>
);

// Graph Analyst - network nodes
export const GraphMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <line x1="6" y1="6" x2="18" y2="6" stroke={COLORS.graphAnalyst} strokeWidth="1.5" />
    <line x1="6" y1="6" x2="12" y2="18" stroke={COLORS.graphAnalyst} strokeWidth="1.5" />
    <line x1="18" y1="6" x2="12" y2="18" stroke={COLORS.graphAnalyst} strokeWidth="1.5" />
    <circle cx="6" cy="6" r="3" fill={COLORS.graphAnalyst} />
    <circle cx="18" cy="6" r="3" fill={COLORS.graphAnalyst} />
    <circle cx="12" cy="18" r="3" fill={COLORS.graphAnalyst} />
  </svg>
);

// Threat Assessor - shield with exclamation
export const ThreatMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <path
      d="M12 2 L4 7 L4 13 C4 18 12 22 12 22 C12 22 20 18 20 13 L20 7 Z"
      stroke={COLORS.threatAssessor}
      strokeWidth="2"
      fill="none"
    />
    <line x1="12" y1="8" x2="12" y2="14" stroke={COLORS.threatAssessor} strokeWidth="2.5" strokeLinecap="round" />
    <circle cx="12" cy="17" r="1.5" fill={COLORS.threatAssessor} />
  </svg>
);

// Briefing Drafter - document with seal
export const BriefingMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <rect x="4" y="2" width="16" height="20" rx="2" stroke={COLORS.briefingDrafter} strokeWidth="2" fill="none" />
    <line x1="8" y1="7" x2="16" y2="7" stroke={COLORS.briefingDrafter} strokeWidth="1.5" opacity={0.6} />
    <line x1="8" y1="11" x2="16" y2="11" stroke={COLORS.briefingDrafter} strokeWidth="1.5" opacity={0.6} />
    <line x1="8" y1="15" x2="13" y2="15" stroke={COLORS.briefingDrafter} strokeWidth="1.5" opacity={0.6} />
    <circle cx="16" cy="17" r="2.5" fill={COLORS.briefingDrafter} opacity={0.8} />
  </svg>
);

// Coordinator - hub with radiating spokes
export const CoordinatorMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="4" fill={COLORS.coordinator} />
    <line x1="12" y1="2" x2="12" y2="8" stroke={COLORS.coordinator} strokeWidth="2" strokeLinecap="round" />
    <line x1="12" y1="16" x2="12" y2="22" stroke={COLORS.coordinator} strokeWidth="2" strokeLinecap="round" />
    <line x1="2" y1="12" x2="8" y2="12" stroke={COLORS.coordinator} strokeWidth="2" strokeLinecap="round" />
    <line x1="16" y1="12" x2="22" y2="12" stroke={COLORS.coordinator} strokeWidth="2" strokeLinecap="round" />
    <line x1="5" y1="5" x2="9" y2="9" stroke={COLORS.coordinator} strokeWidth="1.5" strokeLinecap="round" opacity={0.5} />
    <line x1="15" y1="15" x2="19" y2="19" stroke={COLORS.coordinator} strokeWidth="1.5" strokeLinecap="round" opacity={0.5} />
  </svg>
);

// Ontology Store - hexagon honeycomb
export const OntologyMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <polygon
      points="12,2 20,7 20,17 12,22 4,17 4,7"
      stroke={COLORS.coordinator}
      strokeWidth="1.5"
      fill="none"
      opacity={0.6}
    />
    <polygon
      points="12,6 16,9 16,15 12,18 8,15 8,9"
      stroke={COLORS.coordinator}
      strokeWidth="1.5"
      fill={`${COLORS.coordinator}22`}
    />
    <circle cx="12" cy="12" r="2" fill={COLORS.coordinator} />
  </svg>
);

// LangGraph - connected graph nodes
export const LangGraphMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="6" cy="6" r="3" fill={COLORS.langGraph} />
    <circle cx="18" cy="6" r="3" fill={COLORS.langGraph} />
    <circle cx="12" cy="18" r="3" fill={COLORS.langGraph} />
    <line x1="6" y1="9" x2="12" y2="15" stroke={COLORS.langGraph} strokeWidth="1.5" />
    <line x1="18" y1="9" x2="12" y2="15" stroke={COLORS.langGraph} strokeWidth="1.5" />
    <line x1="9" y1="6" x2="15" y2="6" stroke={COLORS.langGraph} strokeWidth="1.5" />
  </svg>
);

// GitHub mark
export const GitHubMark: React.FC<MarkProps> = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" stroke={COLORS.github} strokeWidth="1.5" fill="none" />
    <circle cx="12" cy="8" r="2" fill={COLORS.github} />
    <circle cx="8" cy="16" r="2" fill={COLORS.github} />
    <circle cx="16" cy="16" r="2" fill={COLORS.github} />
    <line x1="12" y1="10" x2="8" y2="14" stroke={COLORS.github} strokeWidth="1.5" />
    <line x1="12" y1="10" x2="16" y2="14" stroke={COLORS.github} strokeWidth="1.5" />
  </svg>
);

// Python icon
export const PythonIcon: React.FC<MarkProps> = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 14 14">
    <circle cx="5" cy="5" r="4" fill={COLORS.python} opacity={0.7} />
    <circle cx="9" cy="9" r="4" fill={COLORS.python} />
  </svg>
);

// Claude icon
export const ClaudeIcon: React.FC<MarkProps> = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 14 14">
    <circle cx="7" cy="7" r="5" stroke={COLORS.claude} strokeWidth="2" fill="none" />
    <circle cx="7" cy="7" r="2" fill={COLORS.claude} />
  </svg>
);

// Streamlit icon
export const StreamlitIcon: React.FC<MarkProps> = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 14 14">
    <path d="M2 10 L7 2 L12 10" stroke={COLORS.streamlit} strokeWidth="2" fill="none" strokeLinecap="round" />
  </svg>
);

// Agent badge - reusable pill with mark + name
interface AgentBadgeProps {
  name: string;
  color: string;
  mark: React.ReactNode;
  size?: "sm" | "md" | "lg";
}

export const AgentBadge: React.FC<AgentBadgeProps> = ({
  name,
  color,
  mark,
  size = "md",
}) => {
  const sizes = {
    sm: { padding: "3px 8px", fontSize: 11, gap: 4 },
    md: { padding: "6px 14px", fontSize: 14, gap: 6 },
    lg: { padding: "8px 18px", fontSize: 18, gap: 8 },
  };
  const s = sizes[size];

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: s.gap,
        padding: s.padding,
        borderRadius: 20,
        backgroundColor: `${color}22`,
        border: `1px solid ${color}44`,
      }}
    >
      {mark}
      <span style={{ fontSize: s.fontSize, fontWeight: 600, color }}>{name}</span>
    </div>
  );
};

// Tech badge - smaller, for tech stack strip
interface TechBadgeProps {
  name: string;
  color: string;
  mark: React.ReactNode;
}

export const TechBadge: React.FC<TechBadgeProps> = ({ name, color, mark }) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "4px 10px",
      borderRadius: 6,
      backgroundColor: `${color}15`,
      border: `1px solid ${color}30`,
    }}
  >
    {mark}
    <span style={{ fontSize: 12, fontWeight: 500, color: COLORS.textMuted }}>{name}</span>
  </div>
);
