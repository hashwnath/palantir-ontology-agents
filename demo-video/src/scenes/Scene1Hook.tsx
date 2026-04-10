import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import { COLORS, FONTS, TIMING } from "../theme";
import {
  PalantirMark,
  AgentBadge,
  OSINTMark,
  GraphMark,
  ThreatMark,
  BriefingMark,
} from "../components/Logos";
import { Typewriter } from "../components/Typewriter";

const agents = [
  { name: "OSINT", color: COLORS.osint, mark: <OSINTMark size={20} />, angle: -60 },
  { name: "Graph Analyst", color: COLORS.graphAnalyst, mark: <GraphMark size={20} />, angle: -120 },
  { name: "Threat Assessor", color: COLORS.threatAssessor, mark: <ThreatMark size={20} />, angle: 120 },
  { name: "Briefing Drafter", color: COLORS.briefingDrafter, mark: <BriefingMark size={20} />, angle: 60 },
];

export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = TIMING.fps;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.bg,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Palantir mark top-right */}
      <div style={{ position: "absolute", top: 30, right: 30, display: "flex", alignItems: "center", gap: 8 }}>
        <PalantirMark size={32} />
        <span style={{ fontSize: 14, color: COLORS.textDim, fontFamily: FONTS.mono, letterSpacing: "0.1em", textTransform: "uppercase" }}>
          Palantir AIP
        </span>
      </div>

      {/* Subtle grid overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(${COLORS.border}22 1px, transparent 1px), linear-gradient(90deg, ${COLORS.border}22 1px, transparent 1px)`,
          backgroundSize: "80px 80px",
          opacity: interpolate(frame, [0, 30], [0, 0.4], { extrapolateRight: "clamp" }),
        }}
      />

      {/* Center glow */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${COLORS.coordinator}10 0%, transparent 70%)`,
          opacity: interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" }),
        }}
      />

      {/* Agent badges fanning out from center */}
      <div style={{ position: "relative", width: 600, height: 340, marginBottom: 40 }}>
        {agents.map((agent, i) => {
          const delay = i * 5;
          const s = spring({ frame: frame - delay, fps, config: { mass: 0.6, stiffness: 100 } });
          const rad = (agent.angle * Math.PI) / 180;
          const radius = 180;
          const x = 300 + Math.cos(rad) * radius * s - 75;
          const y = 170 + Math.sin(rad) * radius * s - 16;

          return (
            <div
              key={agent.name}
              style={{
                position: "absolute",
                left: x,
                top: y,
                opacity: s,
                transform: `scale(${s})`,
              }}
            >
              <AgentBadge name={agent.name} color={agent.color} mark={agent.mark} size="lg" />
            </div>
          );
        })}

        {/* Center pulse - ontology core */}
        <div
          style={{
            position: "absolute",
            left: 282,
            top: 152,
            width: 36,
            height: 36,
            borderRadius: "50%",
            backgroundColor: COLORS.coordinator,
            opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" }),
            boxShadow: `0 0 ${20 + Math.sin(frame * 0.15) * 10}px ${COLORS.coordinator}66`,
          }}
        />
      </div>

      {/* Headline */}
      <div style={{ textAlign: "center" }}>
        <Typewriter
          text="4 agents. 1 ontology. Intelligence briefing in 2 minutes."
          startFrame={20}
          charsPerFrame={1.2}
          fontSize={52}
          color={COLORS.text}
        />
      </div>

      {/* Scan line effect */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          height: 2,
          top: `${((frame * 3) % 1080)}px`,
          background: `linear-gradient(90deg, transparent, ${COLORS.coordinator}15, transparent)`,
        }}
      />
    </AbsoluteFill>
  );
};
