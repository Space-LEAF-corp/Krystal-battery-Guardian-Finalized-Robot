import argparse
from pathlib import Path
import yaml

from battery import KrystalCoreBattery
from nano_ant_mesh import NanoAntMesh
from firewall import MotionLinkedFirewall
from fluid_robot import FluidRobot

def run_sim(years: float, cfg):
    # Initialize components
    bat = KrystalCoreBattery(
        capacity_ah=cfg["battery"]["baseline_capacity_ah"],
        voltage_v=cfg["battery"]["voltage_v"],
        resistance_ohm=cfg["battery"]["resistance_initial_ohm"],
        coil_durability_pct=100.0,
        resistance_floor_ohm=cfg["battery"]["resistance_floor_ohm"],
        platinum_gain_pct=cfg["battery"]["platinum_film_conductivity_gain_pct"],
        growth_per_year_pct=cfg["battery"]["growth_per_year_pct"],
    )
    mesh = NanoAntMesh(
        eff_min_pct=cfg["mesh"]["efficiency_min_pct"],
        eff_max_pct=cfg["mesh"]["efficiency_max_pct"],
        kinetic_gain_pct=cfg["mesh"]["kinetic_gain_pct"],
        heal_latency_ms=cfg["mesh"]["heal_latency_ms"],
    )
    firewall = MotionLinkedFirewall(
        base_entropy_bits=cfg["robot"]["firewall_base_entropy_bits"]
    )
    robot = FluidRobot(
        mag_track_radius_m=cfg["robot"]["mag_track_radius_m"],
        max_core_speed_mps=cfg["robot"]["max_core_speed_mps"],
        motion_entropy_seed=cfg["robot"]["motion_entropy_seed"],
    )

    total_years = years
    steps = int(total_years) if years >= 1 else 1
    dt_year = total_years / steps

    # Simulation loop
    motion_trace = []
    for step in range(steps):
        # Robot movement influences security and stability
        m = robot.motion_tick(t=step * 1000.0)
        motion_trace.append(m["theta"])

        # Battery annual cycle
        bat.cycle_year()

        # Mesh impact
        eff = mesh.efficiency_pct()
        kinetic = mesh.kinetic_boost(bat.capacity_ah)
        effective_capacity_ah = bat.capacity_ah + kinetic

        # Firewall resilience
        key = firewall.derive_key(motion_trace, mesh_signature=f"eff:{eff:.2f}")
        resilience_pct = firewall.resilience_pct(eff)

    # Final report
    return {
        "years": total_years,
        "capacity_ah": round(effective_capacity_ah, 3),
        "voltage_v": bat.voltage_v,
        "energy_wh": round(effective_capacity_ah * bat.voltage_v, 3),
        "resistance_ohm": round(bat.resistance_ohm, 3),
        "coil_durability_pct": round(bat.coil_durability_pct, 2),
        "mesh_efficiency_pct": round(eff, 2),
        "firewall_resilience_pct": round(resilience_pct, 2),
        "last_key": key[:32]
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=float, default=0.999, help="Simulation horizon in years (e.g., 0.999, 10, 100)")
    parser.add_argument("--config", type=str, default=str(Path(__file__).resolve().parents[1] / "config" / "settings.yaml"))
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    report = run_sim(args.years, cfg)

    print("=== Krystal Core Battery Guardian — Simulation Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
