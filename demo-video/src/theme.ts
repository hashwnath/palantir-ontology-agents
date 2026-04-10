export const COLORS = {
  bg: "#0D0D0D",
  bgLight: "#1A1A1A",
  bgCard: "#141414",
  text: "#E8E8E8",
  textMuted: "#888888",
  textDim: "#555555",

  // Palantir brand
  palantirDark: "#101820",
  palantirMark: "#FFFFFF",

  // Agent colors
  osint: "#4ADE80",
  graphAnalyst: "#60A5FA",
  threatAssessor: "#F59E0B",
  briefingDrafter: "#A78BFA",
  coordinator: "#E879F9",

  // Status
  live: "#4ADE80",
  scaffolded: "#F59E0B",
  error: "#EF4444",

  // Tech
  langGraph: "#4ADE80",
  claude: "#D97706",
  streamlit: "#FF4B4B",
  python: "#3776AB",
  github: "#FFFFFF",

  // Accents
  glow: "rgba(232, 121, 249, 0.12)",
  border: "#2A2A2A",
  borderLight: "rgba(255, 255, 255, 0.08)",
} as const;

export const FONTS = {
  heading: "Inter",
  body: "Inter",
  mono: "JetBrains Mono",
} as const;

export const TIMING = {
  fps: 30,
  totalFrames: 1800, // 60s
  scene1: { start: 0, duration: 150 },
  scene2: { start: 150, duration: 300 },
  scene3: { start: 450, duration: 600 },
  scene4: { start: 1050, duration: 600 },
  scene5: { start: 1650, duration: 150 },
} as const;
