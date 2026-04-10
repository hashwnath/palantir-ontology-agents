import { Composition } from "remotion";
import { Main } from "./Main";
import { TIMING } from "./theme";

export const Root: React.FC = () => {
  return (
    <Composition
      id="Main"
      component={Main}
      durationInFrames={TIMING.totalFrames}
      fps={TIMING.fps}
      width={1920}
      height={1080}
    />
  );
};
