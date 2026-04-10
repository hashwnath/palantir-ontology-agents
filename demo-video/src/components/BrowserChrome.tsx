import { COLORS } from "../theme";

interface BrowserChromeProps {
  url?: string;
  children: React.ReactNode;
}

export const BrowserChrome: React.FC<BrowserChromeProps> = ({
  url = "localhost:8501",
  children,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        borderRadius: 12,
        overflow: "hidden",
        border: `1px solid ${COLORS.border}`,
        backgroundColor: COLORS.bgCard,
      }}
    >
      {/* Title bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          padding: "10px 16px",
          backgroundColor: COLORS.bgLight,
          gap: 8,
        }}
      >
        <div style={{ display: "flex", gap: 6 }}>
          <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: "#EF4444" }} />
          <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: "#F59E0B" }} />
          <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: "#22C55E" }} />
        </div>
        <div
          style={{
            flex: 1,
            backgroundColor: COLORS.bg,
            borderRadius: 6,
            padding: "4px 12px",
            fontSize: 13,
            color: COLORS.textDim,
            fontFamily: "monospace",
          }}
        >
          {url}
        </div>
      </div>
      {/* Content */}
      <div style={{ flex: 1, overflow: "hidden", position: "relative" }}>
        {children}
      </div>
    </div>
  );
};
