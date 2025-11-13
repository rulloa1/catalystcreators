"""
YouTube Horror Content Assistant
Core modules package
"""

__version__ = "1.0.0"
__author__ = "Horror Content Assistant"

from .config_manager import ConfigManager
from .database import ContentDatabase
from .openai_client import OpenAIClient
from .channel_setup import ChannelSetup
from .content_planning import ContentPlanner
from .script_generator import ScriptGenerator
from .metadata_generator import MetadataGenerator
from .scene_planner import ScenePlanner
from .exporter import ContentExporter
from .template_manager import TemplateManager

__all__ = [
    'ConfigManager',
    'ContentDatabase',
    'OpenAIClient',
    'ChannelSetup',
    'ContentPlanner',
    'ScriptGenerator',
    'MetadataGenerator',
    'ScenePlanner',
    'ContentExporter',
    'TemplateManager'
]
