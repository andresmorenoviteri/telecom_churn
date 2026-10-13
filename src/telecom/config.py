from pathlib import Path
import yaml

CONF_DIR = Path(__file__).resolve().parents[2] / "conf" /"base"

def _load_yaml(filename: str) -> dict:
    """Load a YAML file and return its contents as a dictionary."""
    file_path = CONF_DIR / filename
    with open(file_path, "r") as f:
        return yaml.safe_load(f) or {}

def load_catalog() -> dict:
    """Load the catalog configuration from the YAML file."""
    return _load_yaml("catalog.yaml")

def load_parameters() -> dict:
    """Merge all the parameters_*.yml into one dictionary."""
    params = {}
    for file in CONF_DIR.glob("parameters_*.yml"):
        params.update(_load_yaml(file.name))
    return params

