import hashlib
import os
from dataclasses import dataclass

@dataclass
class MotionLinkedFirewall:
    base_entropy_bits: int

    def derive_key(self, motion_trace: list, mesh_signature: str) -> str:
        # Combine motion telemetry with mesh pattern for key material
        h = hashlib.sha256()
        h.update(str(motion_trace).encode())
        h.update(mesh_signature.encode())
        h.update(os.urandom(self.base_entropy_bits // 8))
        return h.hexdigest()

    def resilience_pct(self, mesh_efficiency_pct: float) -> float:
        # Firewall resilience scales with mesh efficiency and entropy
        entropy_factor = min(1.0, self.base_entropy_bits / 256.0)
        return max(0.0, min(100.0, mesh_efficiency_pct * (0.9 + 0.1 * entropy_factor)))
