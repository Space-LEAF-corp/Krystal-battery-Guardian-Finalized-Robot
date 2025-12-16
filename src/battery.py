from dataclasses import dataclass

@dataclass
class KrystalCoreBattery:
    capacity_ah: float            # current capacity in Ah
    voltage_v: float              # nominal voltage
    resistance_ohm: float         # internal resistance
    coil_durability_pct: float    # copper coil durability
    resistance_floor_ohm: float   # minimum achievable resistance
    platinum_gain_pct: float      # thin film conductivity gain
    growth_per_year_pct: float    # growth factor (% per year)

    def cycle_year(self):
        # Capacity growth (compounded)
        self.capacity_ah *= (1.0 + self.growth_per_year_pct / 100.0)

        # Resistance drop towards floor
        drop = (self.resistance_ohm - self.resistance_floor_ohm) * 0.35
        self.resistance_ohm = max(self.resistance_floor_ohm, self.resistance_ohm - drop)

        # Platinum film minor boost each year
        self.capacity_ah *= (1.0 + self.platinum_gain_pct / 100.0)

        # Coil durability degrades slowly (bidirectional coils soften impact)
        self.coil_durability_pct = max(0.0, self.coil_durability_pct - 0.35)

    def energy_wh(self) -> float:
        return self.capacity_ah * self.voltage_v
