"""
Aetheris — Utilities
Config loader, constants, AQI health mappings.
"""

import yaml
from pathlib import Path
import os


def get_project_root():
    """Get project root (where config/ lives)."""
    # Walk up from this file: src/utils/__init__.py -> src -> project_root
    return Path(__file__).resolve().parent.parent.parent


def load_config(config_path=None):
    """Load config.yaml."""
    if config_path is None:
        config_path = get_project_root() / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def ensure_dirs():
    """Create output directories if they don't exist."""
    root = get_project_root()
    for d in ["data/processed", "reports/figures", "models"]:
        os.makedirs(root / d, exist_ok=True)


# ─── AQI Health Advisory Constants ─────────────────────────────

AQI_HEALTH_ADVICE = {
    "Good": {
        "range": "0-50",
        "message": "Air quality is satisfactory. Safe for all outdoor activities.",
        "color": "#00B050",
        "risk": "Minimal",
        "best_time": "Anytime — air quality is great."
    },
    "Satisfactory": {
        "range": "51-100",
        "message": "Acceptable quality. Sensitive individuals should limit prolonged outdoor exertion.",
        "color": "#92D050",
        "risk": "Low",
        "best_time": "Anytime — generally safe."
    },
    "Moderate": {
        "range": "101-200",
        "message": "Breathing discomfort for sensitive groups. Reduce prolonged outdoor activities.",
        "color": "#FFFF00",
        "risk": "Moderate",
        "best_time": "Early morning (6-8 AM) when pollution is typically lower."
    },
    "Poor": {
        "range": "201-300",
        "message": "Breathing discomfort likely for most. Avoid outdoor exercise.",
        "color": "#FF9900",
        "risk": "High",
        "best_time": "Stay indoors. If unavoidable, early morning with a mask."
    },
    "Very Poor": {
        "range": "301-400",
        "message": "Respiratory illness on prolonged exposure. Avoid all outdoor activities.",
        "color": "#FF0000",
        "risk": "Very High",
        "best_time": "Do not go outdoors without protection."
    },
    "Severe": {
        "range": "401-500",
        "message": "Health emergency. Stay indoors with air purifier.",
        "color": "#990000",
        "risk": "Critical",
        "best_time": "Stay indoors. Seal windows. Use air purifier."
    }
}

# Indian seasons by month
SEASON_MAP = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
    10: "Autumn", 11: "Autumn"
}

# AQI color palette for plots
AQI_COLORS = {
    "Good": "#00B050", "Satisfactory": "#92D050",
    "Moderate": "#FFFF00", "Poor": "#FF9900",
    "Very Poor": "#FF0000", "Severe": "#990000"
}

AQI_CATEGORY_ORDER = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
