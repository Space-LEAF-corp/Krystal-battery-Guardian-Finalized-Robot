import yaml
from src.simulation import run_sim

def test_365_day_horizon():
    cfg = yaml.safe_load(open("config/settings.yaml"))
    report = run_sim(0.999, cfg)
    assert report["capacity_ah"] > cfg["battery"]["baseline_capacity_ah"]

def test_10_year_horizon():
    cfg = yaml.safe_load(open("config/settings.yaml"))
    report = run_sim(10, cfg)
    assert report["firewall_resilience_pct"] >= cfg["mesh"]["efficiency_min_pct"] * 0.9

def test_100_year_horizon():
    cfg = yaml.safe_load(open("config/settings.yaml"))
    report = run_sim(100, cfg)
    assert report["coil_durability_pct"] > 0
