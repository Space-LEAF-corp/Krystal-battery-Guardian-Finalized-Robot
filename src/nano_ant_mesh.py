import random
from dataclasses import dataclass

@dataclass
class NanoAntMesh:
    eff_min_pct: float
    eff_max_pct: float
    kinetic_gain_pct: float
    heal_latency_ms: int

    def efficiency_pct(self) -> float:
        # Dynamic efficiency band, pseudo‑random within bounds
        return random.uniform(self.eff_min_pct, self.eff_max_pct)

    def kinetic_boost(self, capacity_ah: float) -> float:
        # Kinetic harvesting adds a small percentage to effective capacity
        return capacity_ah * (self.kinetic_gain_pct / 100.0)
