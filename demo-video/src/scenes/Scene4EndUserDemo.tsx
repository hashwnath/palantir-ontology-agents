import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import { COLORS, FONTS, TIMING } from "../theme";
import { BrowserChrome } from "../components/BrowserChrome";
import { PalantirMark, OSINTMark, GraphMark, ThreatMark, BriefingMark } from "../components/Logos";

const queryText = "Track supply chain disruptions in Taiwan Strait, assess partner exposure, draft SECDEF briefing";

const timelineEvents = [
  { agent: "Coordinator", color: COLORS.coordinator, text: "Parsed query, target: Taiwan Strait supply chain", frame: 80 },
  { agent: "OSINT", color: COLORS.osint, text: "Searching: Taiwan Strait shipping disruptions...", frame: 100 },
  { agent: "Graph Analyst", color: COLORS.graphAnalyst, text: "Traversing: supply chain dependency graph...", frame: 108 },
  { agent: "OSINT", color: COLORS.osint, text: "Completed (6.1s)", frame: 200 },
  { agent: "Graph Analyst", color: COLORS.graphAnalyst, text: "Completed (3.4s)", frame: 220 },
  { agent: "Threat Assessor", color: COLORS.threatAssessor, text: "Assessing risk matrix...", frame: 240 },
  { agent: "Threat Assessor", color: COLORS.threatAssessor, text: "Completed (2.8s)", frame: 300 },
  { agent: "Briefing Drafter", color: COLORS.briefingDrafter, text: "Generating executive briefing...", frame: 320 },
  { agent: "Briefing Drafter", color: COLORS.briefingDrafter, text: "Completed (9.2s)", frame: 420 },
];

export const Scene4EndUserDemo: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = TIMING.fps;

  const browserSlide = spring({ frame, fps, config: { mass: 0.6, stiffness: 80 } });
  const typedChars = Math.min(queryText.length, Math.max(0, Math.floor((frame - 30) * 1.2)));
  const queryTyped = queryText.slice(0, typedChars);
  const buttonClicked = frame > 70;
  const showResults = frame > 250;
  const showBriefing = frame > 430;
  const showComplete = frame > 500;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {/* Palantir mark */}
      <div style={{ position: "absolute", top: 20, right: 30, display: "flex", alignItems: "center", gap: 8, zIndex: 10 }}>
        <PalantirMark size={28} />
      </div>

      {/* Browser chrome with Streamlit UI */}
      <div
        style={{
          position: "absolute",
          top: 30,
          left: 60,
          right: 60,
          bottom: 60,
          opacity: browserSlide,
          transform: `translateY(${(1 - browserSlide) * 40}px)`,
        }}
      >
        <BrowserChrome url="localhost:8501 - Ontology Agent Orchestrator">
          <div style={{ display: "flex", height: "100%", backgroundColor: COLORS.bg }}>
            {/* Main content area */}
            <div style={{ flex: 1, padding: 24, display: "flex", flexDirection: "column", gap: 14, overflow: "hidden" }}>
              {/* Header */}
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ fontSize: 22, fontWeight: 700, color: COLORS.text, fontFamily: FONTS.heading }}>
                  Ontology Agent Orchestrator
                </div>
                <div style={{
                  fontSize: 10,
                  color: COLORS.textDim,
                  fontFamily: FONTS.mono,
                  padding: "2px 8px",
                  borderRadius: 4,
                  border: `1px solid ${COLORS.border}`,
                }}>
                  v0.1.0
                </div>
              </div>

              {/* Query input */}
              <div
                style={{
                  padding: "12px 16px",
                  borderRadius: 8,
                  border: `1px solid ${frame > 30 ? COLORS.coordinator + "66" : COLORS.border}`,
                  backgroundColor: COLORS.bgLight,
                  minHeight: 48,
                }}
              >
                <span style={{ fontSize: 13, color: COLORS.text, fontFamily: FONTS.mono }}>
                  {queryTyped}
                  {typedChars < queryText.length && frame % 30 < 18 && (
                    <span style={{ color: COLORS.coordinator }}>|</span>
                  )}
                </span>
              </div>

              {/* Run button */}
              <div
                style={{
                  alignSelf: "flex-start",
                  padding: "8px 24px",
                  borderRadius: 6,
                  backgroundColor: buttonClicked ? COLORS.coordinator : COLORS.bgLight,
                  color: buttonClicked ? COLORS.bg : COLORS.text,
                  fontSize: 13,
                  fontWeight: 600,
                  fontFamily: FONTS.mono,
                  border: `1px solid ${COLORS.coordinator}`,
                  transform: buttonClicked && frame < 75 ? "scale(0.95)" : "scale(1)",
                  letterSpacing: "0.02em",
                }}
              >
                {buttonClicked ? "Running Analysis..." : "Run Analysis"}
              </div>

              {/* Results area */}
              {showResults && (
                <div style={{ display: "flex", flexDirection: "column", gap: 10, overflow: "hidden" }}>
                  <ResultPanel
                    title="OSINT Findings"
                    icon={<OSINTMark size={14} />}
                    color={COLORS.osint}
                    frame={frame}
                    appearFrame={250}
                    content={[
                      "TSMC production delays reported, PLA naval exercises expanded",
                      "Shipping route diversions up 40%",
                      "Insurance premiums for Taiwan Strait transit +180% MoM",
                    ]}
                  />
                  <ResultPanel
                    title="Graph Analysis"
                    icon={<GraphMark size={14} />}
                    color={COLORS.graphAnalyst}
                    frame={frame}
                    appearFrame={290}
                    content={[
                      "3-hop supply chain exposure: 12 US defense contractors affected",
                      "TSMC critical node (betweenness: 0.89)",
                      "Alternative paths: Samsung Foundry (2-hop), Intel Fab (3-hop)",
                    ]}
                  />
                  <ResultPanel
                    title="Threat Assessment"
                    icon={<ThreatMark size={14} />}
                    color={COLORS.threatAssessor}
                    frame={frame}
                    appearFrame={330}
                    content={[
                      "Risk Level: HIGH (0.87 confidence)",
                      "Escalation probability: 0.64",
                      "Recommended posture: ELEVATED MONITORING",
                    ]}
                  />
                </div>
              )}

              {/* Final briefing panel */}
              {showBriefing && (
                <div
                  style={{
                    padding: 14,
                    borderRadius: 8,
                    backgroundColor: `${COLORS.briefingDrafter}08`,
                    border: `1px solid ${COLORS.briefingDrafter}22`,
                    opacity: interpolate(frame, [430, 460], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 700, color: COLORS.briefingDrafter, marginBottom: 6, display: "flex", alignItems: "center", gap: 6 }}>
                    <BriefingMark size={14} /> Executive Briefing - SECDEF
                  </div>
                  <div style={{ fontSize: 11, color: COLORS.text, lineHeight: 1.6, fontFamily: FONTS.body }}>
                    <strong style={{ color: COLORS.textMuted }}>BLUF:</strong> Taiwan Strait supply chain disruption poses HIGH risk to 12 defense programs.
                    TSMC dependency is single-point-of-failure. Recommend accelerating CHIPS Act allocations.
                  </div>
                  <div style={{ fontSize: 10, color: COLORS.textDim, marginTop: 6, fontFamily: FONTS.mono }}>
                    Classification: UNCLASSIFIED // FOUO | 4 sources | 3 recommendations
                  </div>
                </div>
              )}

              {/* Complete badge */}
              {showComplete && (
                <div
                  style={{
                    alignSelf: "flex-start",
                    padding: "6px 16px",
                    borderRadius: 20,
                    backgroundColor: `${COLORS.live}15`,
                    border: `1px solid ${COLORS.live}33`,
                    fontSize: 13,
                    fontWeight: 600,
                    color: COLORS.live,
                    fontFamily: FONTS.mono,
                    opacity: spring({ frame: frame - 500, fps, config: { mass: 0.5 } }),
                  }}
                >
                  Completed in 1m 47s
                </div>
              )}
            </div>

            {/* Timeline sidebar */}
            <div
              style={{
                width: 320,
                borderLeft: `1px solid ${COLORS.border}`,
                padding: 16,
                display: "flex",
                flexDirection: "column",
                gap: 3,
                overflow: "hidden",
                backgroundColor: `${COLORS.bgLight}88`,
              }}
            >
              <div style={{ fontSize: 12, fontWeight: 700, color: COLORS.textDim, marginBottom: 8, fontFamily: FONTS.mono, letterSpacing: "0.08em" }}>
                AGENT ACTIVITY
              </div>
              {timelineEvents.map((evt, i) => {
                const visible = frame > evt.frame;
                if (!visible) return null;
                const opacity = interpolate(frame, [evt.frame, evt.frame + 10], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                });
                const isComplete = evt.text.startsWith("Completed");
                return (
                  <div
                    key={i}
                    style={{
                      fontSize: 10,
                      opacity,
                      fontFamily: FONTS.mono,
                      padding: "3px 0",
                      display: "flex",
                      gap: 4,
                      alignItems: "flex-start",
                    }}
                  >
                    <span style={{
                      color: evt.color,
                      minWidth: 6,
                      display: "inline-block",
                    }}>
                      {isComplete ? "\u2713" : "\u2022"}
                    </span>
                    <span style={{ color: COLORS.textDim }}>{evt.agent}:</span>
                    <span style={{ color: isComplete ? evt.color : COLORS.textMuted }}>{evt.text}</span>
                  </div>
                );
              })}

              {/* Spinner for active agent */}
              {buttonClicked && !showComplete && (
                <div style={{ marginTop: 8, display: "flex", alignItems: "center", gap: 6 }}>
                  <div style={{
                    width: 8,
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: COLORS.coordinator,
                    opacity: 0.5 + Math.sin(frame * 0.2) * 0.5,
                  }} />
                  <span style={{ fontSize: 10, color: COLORS.textDim, fontFamily: FONTS.mono }}>Processing...</span>
                </div>
              )}
            </div>
          </div>
        </BrowserChrome>
      </div>

      {/* Bottom caption */}
      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: interpolate(frame, [100, 130], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <span style={{ fontSize: 15, color: COLORS.textDim, fontFamily: FONTS.body }}>
          Type a query. Four agents coordinate over the ontology. Actionable intelligence in under 2 minutes.
        </span>
      </div>
    </AbsoluteFill>
  );
};

// Result panel sub-component
const ResultPanel: React.FC<{
  title: string;
  icon: React.ReactNode;
  color: string;
  frame: number;
  appearFrame: number;
  content: string[];
}> = ({ title, icon, color, frame, appearFrame, content }) => {
  const opacity = interpolate(frame, [appearFrame, appearFrame + 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        padding: 10,
        borderRadius: 6,
        backgroundColor: `${color}08`,
        border: `1px solid ${color}18`,
        opacity,
        transform: `translateY(${(1 - opacity) * 10}px)`,
      }}
    >
      <div style={{ fontSize: 12, fontWeight: 700, color, marginBottom: 4, display: "flex", alignItems: "center", gap: 4, fontFamily: FONTS.mono }}>
        {icon} {title}
      </div>
      {content.map((line, i) => {
        const lineOpacity = interpolate(frame, [appearFrame + 10 + i * 8, appearFrame + 20 + i * 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div key={i} style={{ fontSize: 11, color: COLORS.textMuted, opacity: lineOpacity, paddingLeft: 8, lineHeight: 1.5 }}>
            {line}
          </div>
        );
      })}
    </div>
  );
};
