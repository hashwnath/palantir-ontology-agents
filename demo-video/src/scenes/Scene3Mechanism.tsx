import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import { COLORS, FONTS, TIMING } from "../theme";
import {
  PalantirMark,
  CoordinatorMark,
  OSINTMark,
  GraphMark,
  ThreatMark,
  BriefingMark,
  OntologyMark,
  AgentBadge,
  TechBadge,
  LangGraphMark,
} from "../components/Logos";

const agentNodes = [
  { name: "OSINT", color: COLORS.osint, mark: <OSINTMark size={18} />, x: 380, y: 200, status: "LIVE" as const },
  { name: "Graph Analyst", color: COLORS.graphAnalyst, mark: <GraphMark size={18} />, x: 1540, y: 200, status: "LIVE" as const },
  { name: "Threat Assessor", color: COLORS.threatAssessor, mark: <ThreatMark size={18} />, x: 380, y: 520, status: "SCAFFOLDED" as const },
  { name: "Briefing Drafter", color: COLORS.briefingDrafter, mark: <BriefingMark size={18} />, x: 1540, y: 520, status: "SCAFFOLDED" as const },
];

export const Scene3Mechanism: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = TIMING.fps;

  const coordAppear = spring({ frame, fps, config: { mass: 0.5, stiffness: 100 } });
  const ontologyAppear = spring({ frame: frame - 15, fps, config: { mass: 0.5, stiffness: 80 } });
  const flowPhase = interpolate(frame, [120, 250], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sequentialPhase = interpolate(frame, [280, 380], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const captionPhase2 = interpolate(frame, [350, 380], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const coordX = 960;
  const coordY = 360;
  const ontologyY = 500;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {/* Grid overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(${COLORS.border}10 1px, transparent 1px), linear-gradient(90deg, ${COLORS.border}10 1px, transparent 1px)`,
          backgroundSize: "80px 80px",
          opacity: 0.3,
        }}
      />

      {/* Palantir mark */}
      <div style={{ position: "absolute", top: 30, right: 30, display: "flex", alignItems: "center", gap: 8 }}>
        <PalantirMark size={32} />
      </div>

      {/* Title + LangGraph badge */}
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 60,
          opacity: coordAppear,
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <TechBadge name="LangGraph" color={COLORS.langGraph} mark={<LangGraphMark size={16} />} />
        <span style={{ fontSize: 18, color: COLORS.textMuted, fontFamily: FONTS.body }}>
          Coordinator-Specialist Pattern
        </span>
      </div>

      {/* Coordinator hub center */}
      <div
        style={{
          position: "absolute",
          left: coordX,
          top: coordY,
          transform: `translate(-50%, -50%) scale(${coordAppear})`,
          opacity: coordAppear,
        }}
      >
        <div
          style={{
            width: 130,
            height: 130,
            borderRadius: "50%",
            backgroundColor: `${COLORS.coordinator}15`,
            border: `3px solid ${COLORS.coordinator}`,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: `0 0 ${30 + Math.sin(frame * 0.1) * 15}px ${COLORS.coordinator}33`,
          }}
        >
          <CoordinatorMark size={36} />
          <span style={{ fontSize: 12, color: COLORS.coordinator, fontWeight: 600, marginTop: 4, fontFamily: FONTS.mono }}>
            Coordinator
          </span>
        </div>
      </div>

      {/* Ontology Store hexagon below coordinator */}
      <div
        style={{
          position: "absolute",
          left: coordX,
          top: ontologyY + 60,
          transform: `translate(-50%, -50%) scale(${ontologyAppear})`,
          opacity: ontologyAppear,
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 6,
          }}
        >
          <svg width={80} height={80} viewBox="0 0 80 80">
            <polygon
              points="40,4 72,22 72,58 40,76 8,58 8,22"
              stroke={COLORS.coordinator}
              strokeWidth="2"
              fill={`${COLORS.coordinator}10`}
              opacity={0.8}
            />
            <polygon
              points="40,18 58,28 58,48 40,58 22,48 22,28"
              stroke={COLORS.coordinator}
              strokeWidth="1.5"
              fill={`${COLORS.coordinator}15`}
              opacity={0.6}
            />
            <circle cx="40" cy="38" r="5" fill={COLORS.coordinator} opacity={0.8} />
          </svg>
          <span style={{ fontSize: 12, color: COLORS.coordinator, fontFamily: FONTS.mono, fontWeight: 600, letterSpacing: "0.05em" }}>
            ONTOLOGY STORE
          </span>
        </div>
      </div>

      {/* Connection: Coordinator to Ontology Store */}
      <svg style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}>
        <line
          x1={coordX}
          y1={coordY + 65}
          x2={coordX}
          y2={ontologyY + 20}
          stroke={COLORS.coordinator}
          strokeWidth={2}
          strokeDasharray="6 3"
          opacity={ontologyAppear * 0.5}
        />
      </svg>

      {/* Agent nodes + connection lines */}
      {agentNodes.map((agent, i) => {
        const delay = i * 8;
        const s = spring({ frame: frame - 30 - delay, fps, config: { mass: 0.5, stiffness: 80 } });

        const lineProgress = interpolate(frame, [120 + i * 15, 200 + i * 15], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        // Parallel phase: OSINT + Graph Analyst run simultaneously
        const isParallel = i < 2;
        // Sequential phase: Threat -> Briefing
        const isSequential = i >= 2;

        const pulseActive = isParallel
          ? frame > 150 && frame < 300
          : isSequential && i === 2
            ? frame > 280 && frame < 380
            : frame > 360 && frame < 460;

        const pulse = pulseActive ? 1 + Math.sin(frame * 0.2 + i) * 0.05 : 1;

        // Arrow showing sequential flow from Threat -> Briefing
        const seqArrowOpacity = i === 2 ? sequentialPhase * 0.6 : 0;

        return (
          <div key={agent.name}>
            {/* Connection line from coordinator */}
            <svg
              style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }}
            >
              <line
                x1={coordX}
                y1={coordY}
                x2={coordX + (agent.x - coordX) * lineProgress}
                y2={coordY + (agent.y - coordY) * lineProgress}
                stroke={agent.color}
                strokeWidth={2}
                strokeDasharray={lineProgress < 1 ? "8 4" : "none"}
                opacity={lineProgress * 0.5}
              />
              {/* Data flow dots */}
              {pulseActive && (
                <circle
                  cx={coordX + (agent.x - coordX) * ((frame * 0.02 + i * 0.3) % 1)}
                  cy={coordY + (agent.y - coordY) * ((frame * 0.02 + i * 0.3) % 1)}
                  r={4}
                  fill={agent.color}
                  opacity={0.8}
                />
              )}
              {/* Sequential arrow Threat -> Briefing */}
              {i === 2 && (
                <line
                  x1={agent.x + 80}
                  y1={agent.y}
                  x2={agent.x + 80 + (agentNodes[3].x - agent.x - 160) * sequentialPhase}
                  y2={agent.y}
                  stroke={COLORS.textDim}
                  strokeWidth={1.5}
                  strokeDasharray="6 3"
                  opacity={seqArrowOpacity}
                />
              )}
            </svg>

            {/* Agent node */}
            <div
              style={{
                position: "absolute",
                left: agent.x - 80,
                top: agent.y - 30,
                opacity: s,
                transform: `scale(${s * pulse})`,
              }}
            >
              <div
                style={{
                  padding: "12px 20px",
                  borderRadius: 12,
                  backgroundColor: `${agent.color}10`,
                  border: `2px solid ${agent.color}33`,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 6,
                }}
              >
                <AgentBadge name={agent.name} color={agent.color} mark={agent.mark} />
                <span
                  style={{
                    fontSize: 11,
                    fontFamily: FONTS.mono,
                    color: agent.status === "LIVE" ? COLORS.live : COLORS.scaffolded,
                    fontWeight: 600,
                    letterSpacing: "0.08em",
                  }}
                >
                  {agent.status}
                </span>
              </div>
            </div>
          </div>
        );
      })}

      {/* Parallel indicator bracket */}
      <div
        style={{
          position: "absolute",
          top: 140,
          left: 380,
          right: 380,
          opacity: interpolate(frame, [160, 180], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) *
            interpolate(frame, [280, 300], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          textAlign: "center",
        }}
      >
        <span style={{ fontSize: 13, color: COLORS.textDim, fontFamily: FONTS.mono }}>
          PARALLEL EXECUTION
        </span>
      </div>

      {/* Sequential indicator */}
      <div
        style={{
          position: "absolute",
          top: 460,
          left: "50%",
          transform: "translateX(-50%)",
          opacity: sequentialPhase,
          textAlign: "center",
        }}
      >
        <span style={{ fontSize: 13, color: COLORS.textDim, fontFamily: FONTS.mono }}>
          SEQUENTIAL: Threat Assessor → Briefing Drafter
        </span>
      </div>

      {/* Caption line 1 */}
      <div
        style={{
          position: "absolute",
          bottom: 90,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: interpolate(frame, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <span style={{ fontSize: 24, color: COLORS.text, fontFamily: FONTS.body, fontWeight: 600 }}>
          Ontology-first. Agents traverse the graph, not raw data.
        </span>
      </div>

      {/* Caption line 2 */}
      <div
        style={{
          position: "absolute",
          bottom: 50,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: captionPhase2,
        }}
      >
        <span style={{ fontSize: 18, color: COLORS.textMuted, fontFamily: FONTS.body }}>
          OSINT + Graph Analyst run live. Threat + Briefing scaffolded with clean integration points.
        </span>
      </div>
    </AbsoluteFill>
  );
};
