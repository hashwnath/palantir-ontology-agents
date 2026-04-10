import { AbsoluteFill, useCurrentFrame, spring, interpolate } from "remotion";
import { COLORS, FONTS, TIMING } from "../theme";
import { PalantirMark } from "../components/Logos";

const intelSources = [
  { label: "Satellite Feeds", x: 80, y: 100, w: 260, delay: 0 },
  { label: "News Wires", x: 420, y: 60, w: 220, delay: 4 },
  { label: "SIGINT", x: 750, y: 120, w: 180, delay: 8 },
  { label: "HUMINT", x: 140, y: 320, w: 200, delay: 12 },
  { label: "Open Web", x: 480, y: 350, w: 220, delay: 16 },
  { label: "Classified DB", x: 820, y: 300, w: 250, delay: 20 },
];

export const Scene2Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = TIMING.fps;

  const collapseStart = 200;
  const collapseProgress = interpolate(frame, [collapseStart, collapseStart + 40], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Clock counting up to 4 hours
  const clockMinutes = Math.min(240, Math.floor(frame * 1.6));
  const hours = Math.floor(clockMinutes / 60);
  const mins = clockMinutes % 60;
  const clockDisplay = `${hours}h ${mins.toString().padStart(2, "0")}m`;

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {/* Grid overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(${COLORS.border}15 1px, transparent 1px), linear-gradient(90deg, ${COLORS.border}15 1px, transparent 1px)`,
          backgroundSize: "80px 80px",
          opacity: 0.3,
        }}
      />

      {/* Palantir mark */}
      <div style={{ position: "absolute", top: 30, right: 30, display: "flex", alignItems: "center", gap: 8 }}>
        <PalantirMark size={32} />
      </div>

      {/* Scattered intelligence source cards */}
      <div style={{ position: "absolute", top: 40, left: 200, width: 1200, height: 500 }}>
        {intelSources.map((src) => {
          const s = spring({ frame: frame - src.delay, fps, config: { mass: 0.5, stiffness: 120 } });
          const shake = collapseProgress > 0 ? Math.sin(frame * 0.5 + src.delay) * 6 * (1 - collapseProgress) : 0;

          return (
            <div
              key={src.label}
              style={{
                position: "absolute",
                left: src.x + shake,
                top: src.y,
                width: src.w,
                opacity: s * (1 - collapseProgress * 0.7),
                transform: `scale(${s * (1 - collapseProgress * 0.3)}) rotate(${shake * 0.5}deg)`,
              }}
            >
              <div
                style={{
                  backgroundColor: COLORS.bgLight,
                  border: `1px solid ${collapseProgress > 0.5 ? COLORS.error + "88" : COLORS.border}`,
                  borderRadius: 8,
                  padding: "14px 18px",
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: collapseProgress > 0.5 ? COLORS.error : COLORS.textDim,
                    boxShadow: collapseProgress > 0.5 ? `0 0 6px ${COLORS.error}` : "none",
                  }}
                />
                <span style={{ fontSize: 14, color: COLORS.text, fontFamily: FONTS.mono, letterSpacing: "0.02em" }}>
                  {src.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Clock counting up */}
      <div
        style={{
          position: "absolute",
          top: 560,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 8,
          opacity: interpolate(frame, [30, 50], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <div
          style={{
            fontSize: 80,
            fontFamily: FONTS.mono,
            fontWeight: 700,
            color: COLORS.error,
            letterSpacing: "0.05em",
            textShadow: `0 0 30px ${COLORS.error}44`,
          }}
        >
          {clockDisplay}
        </div>
        <span style={{ fontSize: 16, color: COLORS.error, fontFamily: FONTS.mono, opacity: 0.7 }}>
          manual analysis
        </span>
      </div>

      {/* Bottom text */}
      <div
        style={{
          position: "absolute",
          bottom: 70,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: interpolate(frame, [80, 100], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <span style={{ fontSize: 28, color: COLORS.textMuted, fontFamily: FONTS.body, fontWeight: 500 }}>
          Analysts spend 4 hours fusing data from 6 sources.
        </span>
        <br />
        <span style={{ fontSize: 20, color: COLORS.textDim, fontFamily: FONTS.body, marginTop: 8, display: "inline-block" }}>
          Most of it stale by brief time.
        </span>
      </div>
    </AbsoluteFill>
  );
};
