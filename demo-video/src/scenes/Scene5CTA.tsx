import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import { COLORS, FONTS, TIMING } from "../theme";
import {
  PalantirMark,
  GitHubMark,
  TechBadge,
  LangGraphMark,
  PythonIcon,
  ClaudeIcon,
  StreamlitIcon,
} from "../components/Logos";

export const Scene5CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = TIMING.fps;

  const mainSpring = spring({ frame, fps, config: { mass: 0.5, stiffness: 100 } });
  const techSpring = spring({ frame: frame - 20, fps, config: { mass: 0.5, stiffness: 80 } });
  const authorSpring = spring({ frame: frame - 40, fps, config: { mass: 0.5, stiffness: 80 } });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.bg,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 32,
      }}
    >
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

      {/* Glow */}
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 400,
          borderRadius: "50%",
          background: `radial-gradient(ellipse, ${COLORS.coordinator}08 0%, transparent 70%)`,
        }}
      />

      {/* Palantir mark */}
      <div style={{ position: "absolute", top: 30, right: 30, display: "flex", alignItems: "center", gap: 8 }}>
        <PalantirMark size={32} />
      </div>

      {/* Tagline */}
      <div
        style={{
          opacity: mainSpring,
          transform: `translateY(${(1 - mainSpring) * 20}px)`,
          textAlign: "center",
        }}
      >
        <div style={{ fontSize: 42, fontWeight: 700, color: COLORS.text, fontFamily: FONTS.heading, marginBottom: 8, letterSpacing: "-0.02em" }}>
          Built for AIP.
        </div>
        <div style={{ fontSize: 18, color: COLORS.textMuted, fontFamily: FONTS.body }}>
          Ontology-first multi-agent coordination. Working code. Graph traversal over typed entities.
        </div>
      </div>

      {/* GitHub CTA pill */}
      <div
        style={{
          opacity: mainSpring,
          transform: `scale(${mainSpring})`,
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "16px 32px",
          borderRadius: 16,
          backgroundColor: `${COLORS.github}08`,
          border: `2px solid ${COLORS.github}22`,
        }}
      >
        <GitHubMark size={28} />
        <span style={{ fontSize: 20, fontWeight: 600, color: COLORS.text, fontFamily: FONTS.mono }}>
          github.com/hashwnath/palantir-ontology-agents
        </span>
      </div>

      {/* Tech stack strip */}
      <div
        style={{
          display: "flex",
          gap: 12,
          opacity: techSpring,
          transform: `translateY(${(1 - techSpring) * 15}px)`,
        }}
      >
        <TechBadge name="Python" color={COLORS.python} mark={<PythonIcon />} />
        <TechBadge name="LangGraph" color={COLORS.langGraph} mark={<LangGraphMark size={14} />} />
        <TechBadge name="Claude" color={COLORS.claude} mark={<ClaudeIcon />} />
        <TechBadge name="Streamlit" color={COLORS.streamlit} mark={<StreamlitIcon />} />
      </div>

      {/* Author */}
      <div
        style={{
          opacity: authorSpring,
          transform: `translateY(${(1 - authorSpring) * 10}px)`,
          textAlign: "center",
        }}
      >
        <div style={{ fontSize: 16, color: COLORS.textMuted, fontFamily: FONTS.body }}>
          Built by <span style={{ color: COLORS.text, fontWeight: 600 }}>Hashwanth Sutharapu</span>
        </div>
        <div style={{ fontSize: 13, color: COLORS.textDim, fontFamily: FONTS.body, marginTop: 4 }}>
          Microsoft Agent Framework (8K+ stars) | awesome-copilot (29K+ stars) | MAQ Software, Bellevue WA
        </div>
      </div>

      {/* Scan line effect */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          height: 1,
          top: `${((frame * 2) % 1080)}px`,
          background: `linear-gradient(90deg, transparent, ${COLORS.coordinator}10, transparent)`,
        }}
      />
    </AbsoluteFill>
  );
};
