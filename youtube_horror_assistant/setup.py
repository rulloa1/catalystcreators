#!/usr/bin/env python3
"""
Setup script for YouTube Horror Content Assistant
Helps users get started quickly
"""

import os
import sys
import json
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    directories = ['config', 'data', 'exports', 'templates', 'modules']

    for dir_name in directories:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_name}")


def create_config():
    """Create configuration file if it doesn't exist"""
    config_file = Path("config/settings.json")

    if config_file.exists():
        print("⚠️  Configuration file already exists")
        return

    config = {
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

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Created configuration file: {config_file}")


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")

    try:
        import openai
        print("✅ openai package installed")
    except ImportError:
        print("❌ openai package not found")
        print("   Run: pip install openai")
        return False

    return True


def setup():
    """Run setup process"""
    print("🎬 YouTube Horror Content Assistant - Setup")
    print("=" * 60)
    print()

    # Create directories
    print("📁 Creating directories...")
    create_directories()
    print()

    # Create config
    print("⚙️  Setting up configuration...")
    create_config()
    print()

    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit config/settings.json and add your OpenAI API key")
    print("2. Run: python main.py")
    print()
    print("Need help? Read README.md or QUICKSTART.md")
    print("=" * 60)


if __name__ == "__main__":
    setup()
