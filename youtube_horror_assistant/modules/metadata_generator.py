"""
Video Metadata Generator for YouTube Horror Assistant
Creates titles, descriptions, tags, and thumbnail prompts
"""

from typing import List, Dict, Any
import re
from .openai_client import OpenAIClient
from .database import ContentDatabase


class MetadataGenerator:
    """Handles video metadata generation for YouTube optimization"""

    def __init__(self, openai_client: OpenAIClient, database: ContentDatabase):
        self.client = openai_client
        self.db = database

    def generate_titles(self, script: str, story_idea: Dict[str, Any], count: int = 5) -> List[str]:
        """Generate clickable, SEO-optimized video titles"""
        # Extract key elements from script
        script_preview = script[:500] if len(script) > 500 else script

        prompt = f"""Generate {count} compelling YouTube video titles for this horror content:

Story Title: {story_idea.get('title', 'Untitled')}
Story Hook: {story_idea.get('hook', '')}
Niche: {story_idea.get('niche', 'horror')}

Script Preview: {script_preview}

Requirements:
- 60-70 characters max (YouTube optimal length)
- Clickable and intriguing
- Include power words (shocking, terrifying, real, true, etc.)
- Create curiosity gap
- SEO-friendly keywords
- Avoid clickbait that misleads
- Each title should have a different approach/angle

Return as JSON:
{{
    "titles": [
        {{
            "title": "The title text",
            "character_count": 65,
            "approach": "what makes this title unique",
            "keywords": ["keyword1", "keyword2"]
        }}
    ]
}}"""

        response = self.client.generate_json_completion(prompt)
        titles = response.get("titles", [])

        return [t.get("title", "") for t in titles]

    def generate_description(self, script: str, story_idea: Dict[str, Any], channel_info: Optional[Dict[str, Any]] = None) -> str:
        """Generate SEO-optimized video description"""
        script_summary = script[:1000] if len(script) > 1000 else script

        channel_cta = ""
        if channel_info:
            channel_cta = f"\n\n🔔 Subscribe to {channel_info.get('name', 'our channel')} for more {channel_info.get('niche', 'horror')} content!"

        prompt = f"""Create a comprehensive YouTube video description for this horror content:

Story: {story_idea.get('title', '')}
Niche: {story_idea.get('niche', 'horror')}

Script Summary: {script_summary}

Structure the description with:
1. Hook (first 2-3 lines before "Show More")
2. Story summary (2-3 paragraphs)
3. Timestamps (if applicable)
4. Call to action (like, comment, subscribe)
5. Social media links section
6. Hashtags (relevant tags)
7. SEO keywords naturally integrated

Requirements:
- First 150 characters are crucial (appear before "show more")
- Engaging and informative
- Include relevant keywords for SEO
- 300-500 words total
- Add placeholder sections for [TIMESTAMPS], [SOCIAL LINKS]

Return the complete description as plain text."""

        description = self.client.generate_completion(prompt, temperature=0.7)

        # Add channel CTA if provided
        if channel_cta:
            description = description + channel_cta

        return description

    def generate_tags(self, script: str, story_idea: Dict[str, Any], include_trending: bool = True) -> List[str]:
        """Generate relevant tags for maximum visibility"""
        prompt = f"""Generate comprehensive YouTube tags for this horror video:

Title: {story_idea.get('title', '')}
Niche: {story_idea.get('niche', 'horror')}
Description: {story_idea.get('description', '')}

Tag categories needed:
1. Broad tags (horror, scary, creepy)
2. Specific niche tags (paranormal, ghost story, etc.)
3. Long-tail tags (3-4 word phrases)
4. Trending horror tags (if applicable)
5. Related topic tags

Requirements:
- 30-40 tags total
- Mix of high, medium, and low competition
- Include exact match keywords
- Relevant to content (no spam tags)
{"- Focus on trending horror topics" if include_trending else ""}

Return as JSON:
{{
    "tags": ["tag1", "tag2", "tag3", ...]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("tags", [])

    def generate_thumbnail_prompts(self, script: str, story_idea: Dict[str, Any], count: int = 5) -> List[Dict[str, str]]:
        """Generate text-to-image prompts for video thumbnails"""
        # Extract key visual moments from script
        script_preview = script[:1000] if len(script) > 1000 else script

        prompt = f"""Create {count} detailed thumbnail image prompts for this horror video:

Title: {story_idea.get('title', '')}
Story: {story_idea.get('description', '')}
Script Preview: {script_preview}

For each thumbnail, create a prompt that would generate an eye-catching, clickable image.

Requirements for each prompt:
- High-quality, professional look
- 16:9 aspect ratio
- Bold, readable text overlay (if applicable)
- Striking visuals that create curiosity
- Horror atmosphere without being too graphic
- YouTube-friendly (no policy violations)
- Distinct from each other

Return as JSON:
{{
    "thumbnail_prompts": [
        {{
            "prompt": "Detailed image generation prompt",
            "style": "photorealistic/artistic/etc",
            "key_elements": ["element1", "element2"],
            "text_overlay": "suggested text for thumbnail",
            "color_scheme": "dark blues and reds"
        }}
    ]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("thumbnail_prompts", [])

    def generate_complete_metadata(self, script: str, story_idea: Dict[str, Any], channel_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate all metadata at once"""
        print("📋 Generating video titles...")
        titles = self.generate_titles(script, story_idea, count=5)

        print("📝 Generating video description...")
        description = self.generate_description(script, story_idea, channel_info)

        print("🏷️  Generating tags...")
        tags = self.generate_tags(script, story_idea, include_trending=True)

        print("🖼️  Generating thumbnail prompts...")
        thumbnail_prompts = self.generate_thumbnail_prompts(script, story_idea, count=5)

        return {
            "titles": titles,
            "description": description,
            "tags": tags,
            "thumbnail_prompts": thumbnail_prompts
        }

    def save_metadata_to_database(self, script_id: int, titles: List[str], description: str, tags: List[str], thumbnail_prompts: List[Dict[str, str]]) -> int:
        """Save metadata to database"""
        # Convert thumbnail prompts to simple list of strings for storage
        thumbnail_prompt_texts = [tp.get("prompt", "") for tp in thumbnail_prompts]

        return self.db.save_video_metadata(
            script_id=script_id,
            titles=titles,
            description=description,
            tags=tags,
            thumbnail_prompts=thumbnail_prompt_texts
        )

    def optimize_title_for_ctr(self, title: str) -> Dict[str, Any]:
        """Analyze and optimize a title for click-through rate"""
        prompt = f"""Analyze this YouTube video title for CTR (click-through rate) potential:

"{title}"

Evaluate:
1. Length (optimal is 60-70 characters)
2. Power words usage
3. Curiosity factor
4. Keyword presence
5. Emotional appeal
6. Clarity vs mystery balance

Provide:
- Score out of 10
- Strengths
- Weaknesses
- Optimized version

Return as JSON:
{{
    "original_title": "{title}",
    "ctr_score": 7.5,
    "character_count": 65,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1"],
    "optimized_title": "improved version",
    "optimization_notes": "what was changed and why"
}}"""

        return self.client.generate_json_completion(prompt)

    def generate_video_timestamps(self, script: str) -> List[Dict[str, str]]:
        """Generate timestamp sections for video description"""
        prompt = f"""Analyze this script and create YouTube timestamp markers:

{script}

Create 5-8 timestamps marking key moments in the story:
- Introduction/Hook
- Major plot points
- Climax
- Resolution

Return as JSON:
{{
    "timestamps": [
        {{
            "time": "0:00",
            "label": "Introduction"
        }},
        {{
            "time": "2:30",
            "label": "The Discovery"
        }}
    ]
}}

Note: Estimate times based on script length and pacing."""

        response = self.client.generate_json_completion(prompt)
        return response.get("timestamps", [])

    def generate_end_screen_suggestions(self, related_videos: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate suggestions for YouTube end screen"""
        prompt = """Suggest an optimal end screen layout for a horror video:

Include:
1. Video recommendations (which related videos to promote)
2. Subscribe button placement
3. Playlist suggestions
4. Call to action text

Return as JSON with specific recommendations."""

        return self.client.generate_json_completion(prompt)

    def create_upload_checklist(self, metadata: Dict[str, Any]) -> List[str]:
        """Create a checklist for video upload"""
        checklist = [
            "✅ Video file exported and ready",
            f"✅ Title selected (from {len(metadata.get('titles', []))} options)",
            "✅ Description copied and customized",
            "✅ Tags added (all relevant tags)",
            "✅ Thumbnail created and uploaded",
            "✅ End screen configured",
            "✅ Cards added (if applicable)",
            "✅ Playlist selected",
            "✅ Visibility set (public/unlisted/private)",
            "✅ Premiere scheduled (if applicable)",
            "✅ Community post prepared",
            "✅ Social media posts drafted",
            "✅ Analytics tracking enabled"
        ]

        return checklist
