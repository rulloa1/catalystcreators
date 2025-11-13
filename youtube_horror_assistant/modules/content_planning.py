"""
Content Planning Module for YouTube Horror Assistant
Generates viral horror story ideas and manages content pipeline
"""

from typing import List, Dict, Any, Optional
from .openai_client import OpenAIClient
from .database import ContentDatabase


class ContentPlanner:
    """Handles content ideation and planning"""

    def __init__(self, openai_client: OpenAIClient, database: ContentDatabase):
        self.client = openai_client
        self.db = database

    def generate_story_ideas(self, niche: str = "paranormal", count: int = 5, target_duration: int = 5, use_trends: bool = True) -> List[Dict[str, Any]]:
        """Generate viral horror story ideas"""
        trends_note = "Focus on currently trending horror topics and viral story formats." if use_trends else ""

        prompt = f"""Generate {count} viral horror story ideas for YouTube in the {niche} sub-niche.

{trends_note}

Target video duration: {target_duration} minutes

For each story idea, provide:
1. A compelling title
2. A detailed description (2-3 paragraphs)
3. A powerful hook to start the story
4. Why it would go viral (engagement potential)
5. Target audience appeal

Horror sub-niche context:
- Paranormal: ghosts, hauntings, supernatural
- Urban legends: modern myths, creepypastas
- True crime: real mysterious cases with horror elements
- Cryptids: mysterious creatures, bigfoot, etc.
- Personal experiences: real-life scary encounters

Return as JSON:
{{
    "ideas": [
        {{
            "title": "Story title",
            "description": "Detailed description",
            "hook": "Opening hook that grabs attention",
            "viral_potential": "Why this would perform well",
            "target_audience": "Who would love this",
            "estimated_duration": {target_duration},
            "niche": "{niche}"
        }}
    ]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("ideas", [])

    def save_ideas_to_database(self, ideas: List[Dict[str, Any]]) -> List[int]:
        """Save generated ideas to database and return IDs"""
        idea_ids = []

        for idea in ideas:
            idea_id = self.db.save_story_idea(
                title=idea.get("title", ""),
                description=idea.get("description", ""),
                niche=idea.get("niche", "horror"),
                hook=idea.get("hook", ""),
                target_duration=idea.get("estimated_duration", 5)
            )
            idea_ids.append(idea_id)

        return idea_ids

    def get_saved_ideas(self, niche: Optional[str] = None, status: str = "pending", limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieve saved story ideas from database"""
        return self.db.get_story_ideas(status=status, niche=niche, limit=limit)

    def refine_story_idea(self, idea: Dict[str, Any], user_feedback: str) -> Dict[str, Any]:
        """Refine a story idea based on user feedback"""
        prompt = f"""Refine this horror story idea based on user feedback:

Original Idea:
Title: {idea.get('title')}
Description: {idea.get('description')}
Hook: {idea.get('hook')}

User Feedback: {user_feedback}

Generate an improved version that addresses the feedback while maintaining the core appeal.

Return as JSON:
{{
    "title": "Refined title",
    "description": "Refined description",
    "hook": "Refined hook",
    "improvements_made": "Summary of changes"
}}"""

        return self.client.generate_json_completion(prompt)

    def expand_story_idea(self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """Expand a story idea with more details for scripting"""
        prompt = f"""Expand this horror story idea into a detailed story outline:

Title: {idea.get('title')}
Description: {idea.get('description')}
Hook: {idea.get('hook')}
Duration: {idea.get('estimated_duration', 5)} minutes

Create a detailed outline including:
1. Story structure (beginning, middle, end)
2. Key plot points and beats
3. Atmosphere and mood descriptions
4. Character details (if applicable)
5. Climax and resolution
6. Visual/audio suggestions

Return as JSON:
{{
    "act_structure": {{
        "act1": "Setup details",
        "act2": "Conflict and development",
        "act3": "Climax and resolution"
    }},
    "key_beats": ["beat1", "beat2", ...],
    "atmosphere": "Mood and atmosphere description",
    "characters": ["character1 description", ...],
    "visual_elements": ["visual1", "visual2", ...],
    "audio_suggestions": ["sound1", "sound2", ...]
}}"""

        return self.client.generate_json_completion(prompt)

    def generate_ideas_by_theme(self, theme: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate story ideas around a specific theme"""
        prompt = f"""Generate {count} horror story ideas centered around the theme: "{theme}"

Each idea should:
- Directly relate to the theme
- Have a unique angle or twist
- Be suitable for YouTube (5-10 minute format)
- Have strong viral potential

Return as JSON:
{{
    "ideas": [
        {{
            "title": "Story title",
            "description": "Detailed description",
            "hook": "Opening hook",
            "theme_connection": "How it relates to {theme}",
            "unique_angle": "What makes this different"
        }}
    ]
}}"""

        response = self.client.generate_json_completion(prompt)
        return response.get("ideas", [])

    def analyze_idea_performance(self, idea_id: int, metrics: Dict[str, Any]) -> None:
        """Store analytics about idea performance"""
        for metric_name, metric_value in metrics.items():
            self.db.save_analytics("story_idea", idea_id, metric_name, str(metric_value))

    def get_top_performing_niches(self) -> List[Dict[str, Any]]:
        """Analyze which niches perform best based on analytics"""
        analytics = self.db.get_analytics(item_type="story_idea")

        # Simple aggregation (can be enhanced)
        niche_performance = {}

        for record in analytics:
            if record.get('metric_name') == 'performance_score':
                # Would need to join with story_ideas table for niche info
                # This is a simplified version
                pass

        return []

    def batch_generate_ideas(self, niches: List[str], count_per_niche: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """Generate ideas for multiple niches at once"""
        results = {}

        for niche in niches:
            print(f"Generating ideas for {niche}...")
            ideas = self.generate_story_ideas(niche=niche, count=count_per_niche)
            results[niche] = ideas

        return results

    def create_content_calendar(self, num_weeks: int = 4, videos_per_week: int = 3) -> Dict[str, Any]:
        """Generate a content calendar with story ideas"""
        total_videos = num_weeks * videos_per_week

        prompt = f"""Create a {num_weeks}-week content calendar for a horror YouTube channel.

Requirements:
- {videos_per_week} videos per week
- Mix of different horror sub-niches
- Strategic variety (don't repeat similar themes back-to-back)
- Balance viral potential with consistent quality
- Consider trending topics and seasonal relevance

Return as JSON:
{{
    "calendar": [
        {{
            "week": 1,
            "videos": [
                {{
                    "day": "Monday",
                    "title": "Video title",
                    "niche": "paranormal",
                    "brief_description": "Short description",
                    "rationale": "Why this video this day"
                }}
            ]
        }}
    ],
    "strategy_notes": "Overall content strategy explanation"
}}"""

        return self.client.generate_json_completion(prompt)
