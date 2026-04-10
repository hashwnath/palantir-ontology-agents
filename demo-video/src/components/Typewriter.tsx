import { useCurrentFrame } from "remotion";
import { COLORS, FONTS } from "../theme";

interface TypewriterProps {
  text: string;
  startFrame?: number;
  charsPerFrame?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  showCursor?: boolean;
}

export const Typewriter: React.FC<TypewriterProps> = ({
  text,
  startFrame = 0,
  charsPerFrame = 0.8,
  fontSize = 48,
  color = COLORS.text,
  fontFamily = FONTS.heading,
  showCursor = true,
}) => {
  const frame = useCurrentFrame();
  const elapsed = Math.max(0, frame - startFrame);
  const chars = Math.min(text.length, Math.floor(elapsed * charsPerFrame));
  const displayText = text.slice(0, chars);
  const cursorVisible = showCursor && frame % 30 < 20;

  return (
    <span
      style={{
        fontSize,
        fontFamily,
        fontWeight: 700,
        color,
        letterSpacing: "-0.02em",
      }}
    >
      {displayText}
      {cursorVisible && chars < text.length && (
        <span style={{ color: COLORS.coordinator, fontWeight: 400 }}>|</span>
      )}
    </span>
  );
};
