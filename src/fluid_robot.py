import math
import random
from dataclasses import dataclass

@dataclass
class FluidRobot:
    mag_track_radius_m: float
    max_core_speed_mps: float
    motion_entropy_seed: int

    def __post_init__(self):
        random.seed(self.motion_entropy_seed)

    def motion_tick(self, t: float) -> dict:
        # Pseudo‑random orbital within the track radius
        theta = (t * self.max_core_speed_mps / self.mag_track_radius_m) + random.uniform(-0.5, 0.5)
        x = self.mag_track_radius_m * math.cos(theta)
        y = self.mag_track_radius_m * math.sin(theta)
        z = self.mag_track_radius_m * math.sin(theta / 2.0)

        # Gyro stability metric (lower is better wobble)
        wobble = abs(math.sin(theta)) * random.uniform(0.1, 0.3)

        return {
            "pos": (x, y, z),
            "wobble": wobble,
            "theta": theta
        }
