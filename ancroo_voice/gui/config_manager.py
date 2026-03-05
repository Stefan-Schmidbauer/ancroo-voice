"""
GUI Configuration Manager

Handles loading and saving GUI configuration (runtime settings as JSON).
"""

import json
from ..constants import CONFIG_FILE


def load_config():
    """Load configuration from file

    Returns:
        dict: Configuration dictionary
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: config.json is corrupted, resetting to defaults: {e}")
        except (IOError, OSError) as e:
            print(f"Warning: Could not read config: {e}")
    return {}


def save_config(config):
    """Save configuration to file (in project directory)

    Args:
        config: Configuration dictionary to save
    """
    try:
        # Config is saved in project directory - no need to create directory
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except (IOError, OSError) as e:
        print(f"Error saving config: {e}")
