import { AbsoluteFill, Sequence } from "remotion";
import { COLORS, TIMING } from "./theme";
import { Scene1Hook } from "./scenes/Scene1Hook";
import { Scene2Problem } from "./scenes/Scene2Problem";
import { Scene3Mechanism } from "./scenes/Scene3Mechanism";
import { Scene4EndUserDemo } from "./scenes/Scene4EndUserDemo";
import { Scene5CTA } from "./scenes/Scene5CTA";

export const Main: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <Sequence from={TIMING.scene1.start} durationInFrames={TIMING.scene1.duration}>
        <Scene1Hook />
      </Sequence>
      <Sequence from={TIMING.scene2.start} durationInFrames={TIMING.scene2.duration}>
        <Scene2Problem />
      </Sequence>
      <Sequence from={TIMING.scene3.start} durationInFrames={TIMING.scene3.duration}>
        <Scene3Mechanism />
      </Sequence>
      <Sequence from={TIMING.scene4.start} durationInFrames={TIMING.scene4.duration}>
        <Scene4EndUserDemo />
      </Sequence>
      <Sequence from={TIMING.scene5.start} durationInFrames={TIMING.scene5.duration}>
        <Scene5CTA />
      </Sequence>
    </AbsoluteFill>
  );
};
