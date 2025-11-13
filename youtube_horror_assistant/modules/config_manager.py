"""
Configuration Manager for YouTube Horror Assistant
Handles API keys, user preferences, and application settings
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration and settings"""

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "settings.json"
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.create_default_config()

    def create_default_config(self) -> None:
        """Create default configuration file"""
        self.config = {
            "api": {
                "openai_api_key": "",
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 4000
            },
            "paths": {
                "data_dir": "data",
                "exports_dir": "exports",
                "templates_dir": "templates"
            },
            "defaults": {
                "horror_niche": "paranormal",
                "script_duration": 5,
                "num_title_options": 5,
                "num_channel_names": 10
            },
            "preferences": {
                "auto_save": True,
                "export_format": ["json", "markdown"],
                "show_tips": True
            }
        }
        self.save_config()

    def save_config(self) -> None:
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, indent=4, fp=f)

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get("api.openai_api_key")
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        Example: config.set("api.openai_api_key", "sk-...")
        """
        keys = key_path.split('.')
        config_ref = self.config

        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]

        config_ref[keys[-1]] = value
        self.save_config()

    def get_openai_key(self) -> Optional[str]:
        """Get OpenAI API key from config or environment"""
        api_key = self.get("api.openai_api_key")

        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        return api_key if api_key else None

    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate configuration and return status and errors"""
        errors = []

        # Check for API key
        if not self.get_openai_key():
            errors.append("OpenAI API key not configured. Set it in config/settings.json or OPENAI_API_KEY environment variable")

        # Check required directories
        for dir_key in ["data_dir", "exports_dir", "templates_dir"]:
            dir_path = self.get(f"paths.{dir_key}")
            if not dir_path:
                errors.append(f"Missing configuration: paths.{dir_key}")

        return len(errors) == 0, errors

    def display_config(self) -> str:
        """Return formatted configuration for display"""
        display_config = self.config.copy()

        # Mask API key
        if "api" in display_config and "openai_api_key" in display_config["api"]:
            key = display_config["api"]["openai_api_key"]
            if key:
                display_config["api"]["openai_api_key"] = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"

        return json.dumps(display_config, indent=2)
