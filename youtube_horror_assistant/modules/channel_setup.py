"""
Channel Setup Module for YouTube Horror Assistant
Generates channel names, descriptions, keywords, and logo prompts
"""

from typing import List, Dict, Any
from .openai_client import OpenAIClient


class ChannelSetup:
    """Handles channel creation and setup tasks"""

    def __init__(self, openai_client: OpenAIClient):
        self.client = openai_client

    def generate_channel_names(self, niche: str = "horror", count: int = 10, style: str = "mysterious") -> List[str]:
        """Generate channel name options"""
        prompt = f"""Generate {count} unique and catchy YouTube channel names for a {niche} content channel.

Style preference: {style}

Requirements:
- Memorable and easy to spell
- SEO-friendly
- Not too long (2-3 words ideally)
- Available-sounding (avoid obvious trademark conflicts)
- Evocative of {niche} content

Return as JSON:
{{
    "channel_names": ["name1", "name2", ...]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("channel_names", [])

    def generate_channel_description(self, channel_name: str, niche: str = "horror", target_audience: str = "horror enthusiasts") -> Dict[str, Any]:
        """Generate SEO-optimized channel description"""
        prompt = f"""Create a comprehensive YouTube channel description for "{channel_name}", a {niche} content channel targeting {target_audience}.

Include:
1. A compelling hook (first 2-3 sentences)
2. What viewers can expect
3. Upload schedule mention
4. Call to action
5. SEO keywords naturally integrated

Return as JSON:
{{
    "short_description": "brief 1-2 sentence description",
    "full_description": "complete channel description (150-200 words)",
    "about_section": "concise about section text",
    "seo_keywords": ["keyword1", "keyword2", ...]
}}"""

        return self.client.generate_json_completion(prompt)

    def generate_channel_keywords(self, channel_name: str, niche: str = "horror", use_trending: bool = True) -> List[str]:
        """Generate channel keywords for SEO"""
        prompt = f"""Generate a comprehensive list of SEO keywords for a YouTube channel called "{channel_name}" in the {niche} niche.

Requirements:
- Include broad keywords (e.g., "horror stories")
- Include specific keywords (e.g., "true paranormal experiences")
- Include long-tail keywords (e.g., "scary stories told in the dark")
{"- Focus on currently trending horror topics" if use_trending else ""}
- Mix high and medium competition keywords
- Include 25-30 keywords total

Return as JSON:
{{
    "primary_keywords": ["keyword1", "keyword2", ...],
    "secondary_keywords": ["keyword1", "keyword2", ...],
    "long_tail_keywords": ["keyword phrase 1", "keyword phrase 2", ...]
}}"""

        response = self.client.generate_json_completion(prompt)

        # Flatten all keywords into a single list
        all_keywords = []
        all_keywords.extend(response.get("primary_keywords", []))
        all_keywords.extend(response.get("secondary_keywords", []))
        all_keywords.extend(response.get("long_tail_keywords", []))

        return all_keywords

    def generate_logo_prompt(self, channel_name: str, niche: str = "horror", style: str = "dark and mysterious") -> Dict[str, str]:
        """Generate text-to-image prompts for channel logo"""
        prompt = f"""Create detailed text-to-image prompts for a YouTube channel logo for "{channel_name}" in the {niche} niche.

Style: {style}

Generate 3 different prompt variations:
1. Minimalist/modern approach
2. Detailed/illustrative approach
3. Text-focused with visual elements

For each prompt, include:
- Visual elements
- Color scheme
- Style and mood
- Composition notes
- Technical specifications (high quality, transparent background, etc.)

Return as JSON:
{{
    "minimalist_prompt": "detailed prompt...",
    "detailed_prompt": "detailed prompt...",
    "text_focused_prompt": "detailed prompt...",
    "general_guidelines": "color palette and style notes"
}}"""

        return self.client.generate_json_completion(prompt)

    def create_complete_channel_package(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete channel setup package"""
        niche = preferences.get("niche", "horror")
        style = preferences.get("style", "mysterious")
        target_audience = preferences.get("target_audience", "horror enthusiasts")
        num_names = preferences.get("num_channel_names", 10)

        print("🎬 Generating channel names...")
        channel_names = self.generate_channel_names(niche, num_names, style)

        # Use the first generated name as default
        selected_name = preferences.get("channel_name", channel_names[0] if channel_names else "Horror Channel")

        print(f"📝 Generating description for '{selected_name}'...")
        description_data = self.generate_channel_description(selected_name, niche, target_audience)

        print("🔑 Generating SEO keywords...")
        keywords = self.generate_channel_keywords(selected_name, niche, use_trending=True)

        print("🎨 Generating logo prompts...")
        logo_prompts = self.generate_logo_prompt(selected_name, niche, style)

        return {
            "channel_names": channel_names,
            "selected_name": selected_name,
            "description": description_data,
            "keywords": keywords,
            "logo_prompts": logo_prompts,
            "niche": niche,
            "style": style,
            "target_audience": target_audience
        }

    def regenerate_names(self, niche: str, count: int, avoid_names: List[str] = None) -> List[str]:
        """Regenerate channel names, avoiding previously generated ones"""
        avoid_list = "\n".join(avoid_names) if avoid_names else "None"

        prompt = f"""Generate {count} unique YouTube channel names for a {niche} content channel.

AVOID these previously generated names:
{avoid_list}

Requirements:
- Completely different from the avoided names
- Memorable and catchy
- SEO-friendly
- 2-3 words ideally

Return as JSON:
{{
    "channel_names": ["name1", "name2", ...]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("channel_names", [])
