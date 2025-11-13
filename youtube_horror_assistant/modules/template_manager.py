"""
Template Manager for YouTube Horror Assistant
Manages templates for different horror sub-niches
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class TemplateManager:
    """Manages horror niche templates and style guides"""

    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.niches_file = self.templates_dir / "horror_niches.json"
        self.niches = self.load_niches()

    def load_niches(self) -> Dict[str, Any]:
        """Load horror niche templates"""
        if self.niches_file.exists():
            with open(self.niches_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('niches', {})
        return {}

    def get_niche_list(self) -> List[str]:
        """Get list of available niches"""
        return list(self.niches.keys())

    def get_niche_info(self, niche: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific niche"""
        return self.niches.get(niche)

    def get_niche_style_guide(self, niche: str) -> Optional[Dict[str, Any]]:
        """Get style guide for a specific niche"""
        niche_info = self.get_niche_info(niche)
        if niche_info:
            return niche_info.get('style_guide')
        return None

    def get_niche_keywords(self, niche: str) -> List[str]:
        """Get keywords for a specific niche"""
        niche_info = self.get_niche_info(niche)
        if niche_info:
            return niche_info.get('keywords', [])
        return []

    def get_niche_hooks(self, niche: str) -> List[str]:
        """Get common hooks for a specific niche"""
        niche_info = self.get_niche_info(niche)
        if niche_info:
            return niche_info.get('common_hooks', [])
        return []

    def get_visual_style(self, niche: str) -> Optional[str]:
        """Get visual style description for a niche"""
        niche_info = self.get_niche_info(niche)
        if niche_info:
            return niche_info.get('visual_style')
        return None

    def get_thumbnail_elements(self, niche: str) -> List[str]:
        """Get recommended thumbnail elements for a niche"""
        niche_info = self.get_niche_info(niche)
        if niche_info:
            return niche_info.get('thumbnail_elements', [])
        return []

    def display_niche_options(self) -> str:
        """Display all available niches with descriptions"""
        output = "Available Horror Niches:\n\n"

        for i, (key, niche) in enumerate(self.niches.items(), 1):
            output += f"{i}. {niche.get('name', key.title())}\n"
            output += f"   {niche.get('description', '')}\n\n"

        return output

    def get_niche_comparison(self, niche1: str, niche2: str) -> Dict[str, Any]:
        """Compare two niches"""
        info1 = self.get_niche_info(niche1)
        info2 = self.get_niche_info(niche2)

        if not info1 or not info2:
            return {}

        return {
            "niche1": {
                "name": niche1,
                "style": info1.get('style_guide'),
                "visual": info1.get('visual_style')
            },
            "niche2": {
                "name": niche2,
                "style": info2.get('style_guide'),
                "visual": info2.get('visual_style')
            }
        }

    def create_custom_niche(self, name: str, description: str, keywords: List[str], style_guide: Dict[str, Any]) -> None:
        """Create a custom niche template"""
        custom_key = name.lower().replace(' ', '_')

        self.niches[custom_key] = {
            "name": name,
            "description": description,
            "keywords": keywords,
            "style_guide": style_guide,
            "common_hooks": [],
            "visual_style": "custom",
            "thumbnail_elements": []
        }

        self.save_niches()

    def save_niches(self) -> None:
        """Save niches to file"""
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        with open(self.niches_file, 'w', encoding='utf-8') as f:
            json.dump({"niches": self.niches}, f, indent=2, ensure_ascii=False)

    def get_recommendations_for_niche(self, niche: str) -> Dict[str, Any]:
        """Get comprehensive recommendations for a niche"""
        niche_info = self.get_niche_info(niche)

        if not niche_info:
            return {}

        return {
            "niche": niche,
            "name": niche_info.get('name'),
            "style_guide": niche_info.get('style_guide'),
            "recommended_keywords": niche_info.get('keywords'),
            "hook_templates": niche_info.get('common_hooks'),
            "visual_style": niche_info.get('visual_style'),
            "thumbnail_tips": niche_info.get('thumbnail_elements'),
            "best_practices": self._get_best_practices(niche)
        }

    def _get_best_practices(self, niche: str) -> List[str]:
        """Get best practices for a specific niche"""
        practices = {
            "paranormal": [
                "Build atmosphere slowly",
                "Use sensory details (cold spots, strange sounds)",
                "Leave some things unexplained",
                "Focus on emotional impact over jump scares"
            ],
            "urban_legends": [
                "Make it feel relatable and modern",
                "Include multiple versions or perspectives",
                "Build to a twist or unexpected revelation",
                "Use contemporary references"
            ],
            "true_crime": [
                "Stick to facts but present dramatically",
                "Show respect for victims",
                "Present multiple theories when unsolved",
                "Include timeline and context"
            ],
            "cryptids": [
                "Present evidence objectively",
                "Build credibility with research",
                "Create sense of remote, isolated locations",
                "Balance skepticism and belief"
            ],
            "personal_experiences": [
                "Maintain authentic voice",
                "Include specific, believable details",
                "Show emotional reactions realistically",
                "Don't over-explain everything"
            ]
        }

        return practices.get(niche, [
            "Understand your audience",
            "Build atmosphere and tension",
            "Have a clear narrative arc",
            "End with impact"
        ])
