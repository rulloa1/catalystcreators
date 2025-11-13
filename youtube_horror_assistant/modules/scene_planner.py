"""
Scene Planning Module for YouTube Horror Assistant
Breaks down scripts into scenes and generates image/animation prompts
"""

from typing import List, Dict, Any
import re
from .openai_client import OpenAIClient
from .database import ContentDatabase


class ScenePlanner:
    """Handles scene breakdown and visual planning"""

    def __init__(self, openai_client: OpenAIClient, database: ContentDatabase):
        self.client = openai_client
        self.db = database

    def break_down_script(self, script: str, target_scenes: int = None) -> List[Dict[str, Any]]:
        """Break script into scenes with timing"""
        # Calculate word count and duration
        words = len(script.split())
        duration_minutes = words / 150

        scene_count_suggestion = ""
        if target_scenes:
            scene_count_suggestion = f"Create exactly {target_scenes} scenes."
        else:
            # Suggest 1 scene per 30-45 seconds of content
            suggested_scenes = int(duration_minutes * 2)
            scene_count_suggestion = f"Create approximately {suggested_scenes} scenes (1 scene per 30-45 seconds)."

        prompt = f"""Break down this horror script into distinct scenes for video production:

{script}

{scene_count_suggestion}

For each scene:
1. Scene number and title
2. The narration/content for that scene
3. Key visual elements
4. Mood/atmosphere
5. Estimated duration in seconds

Consider:
- Natural story progression
- Visual variety (don't repeat same type of shot)
- Pacing (mix of slow and fast moments)
- Each scene should be 15-45 seconds typically

Return as JSON:
{{
    "total_duration": {duration_minutes},
    "scene_count": 10,
    "scenes": [
        {{
            "scene_number": 1,
            "title": "Scene title",
            "content": "The narration/dialogue for this scene",
            "visual_description": "What we see",
            "mood": "eerie, tense, etc",
            "duration_seconds": 30,
            "key_elements": ["element1", "element2"]
        }}
    ]
}}"""

        return self.client.generate_json_completion(prompt)

    def generate_image_prompts(self, scenes: List[Dict[str, Any]], style: str = "cinematic horror") -> List[Dict[str, Any]]:
        """Generate image generation prompts for each scene"""
        prompts_list = []

        for scene in scenes:
            prompt_request = f"""Create a detailed text-to-image prompt for this horror video scene:

Scene #{scene.get('scene_number')}: {scene.get('title', '')}
Visual Description: {scene.get('visual_description', '')}
Mood: {scene.get('mood', '')}
Key Elements: {', '.join(scene.get('key_elements', []))}

Style: {style}

Generate a detailed prompt for an AI image generator (like Midjourney, DALL-E, or Stable Diffusion).

Requirements:
- Cinematic composition
- Atmospheric lighting
- High quality, detailed
- 16:9 aspect ratio
- Specific enough to be consistent
- Horror atmosphere without being too graphic

Return as JSON:
{{
    "image_prompt": "detailed prompt for image generation",
    "style_tags": "cinematic, moody, atmospheric, etc",
    "technical_specs": "16:9, high detail, photorealistic",
    "color_palette": "dark blues, deep reds, etc",
    "lighting": "dim, shadowy, etc"
}}"""

            result = self.client.generate_json_completion(prompt_request)

            prompts_list.append({
                "scene_number": scene.get('scene_number'),
                "scene_title": scene.get('title'),
                "image_prompt": result.get('image_prompt', ''),
                "full_prompt": f"{result.get('image_prompt', '')} {result.get('style_tags', '')} {result.get('technical_specs', '')}",
                "color_palette": result.get('color_palette', ''),
                "lighting": result.get('lighting', '')
            })

        return prompts_list

    def generate_animation_prompts(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate animation/motion prompts for scenes with movement"""
        animation_prompts = []

        for scene in scenes:
            prompt_request = f"""Create animation/motion instructions for this horror video scene:

Scene: {scene.get('title', '')}
Visual: {scene.get('visual_description', '')}
Duration: {scene.get('duration_seconds', 30)} seconds
Mood: {scene.get('mood', '')}

Suggest:
1. Camera movement (pan, zoom, tilt, static)
2. Subject motion (if any)
3. Transition type (to next scene)
4. Special effects (if needed)
5. Pacing (slow, medium, fast)

Return as JSON:
{{
    "camera_movement": "slow zoom in / pan left / etc",
    "subject_motion": "none / character walks / etc",
    "transition": "fade to black / cut / dissolve",
    "special_effects": ["effect1", "effect2"],
    "pacing": "slow and deliberate",
    "keyframes": "description of key moments in the animation"
}}"""

            result = self.client.generate_json_completion(prompt_request)

            animation_prompts.append({
                "scene_number": scene.get('scene_number'),
                "scene_title": scene.get('title'),
                **result
            })

        return animation_prompts

    def calculate_scene_timings(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate precise timings for each scene"""
        current_time = 0
        timed_scenes = []

        for scene in scenes:
            duration = scene.get('duration_seconds', 30)

            start_time = current_time
            end_time = current_time + duration

            timed_scenes.append({
                **scene,
                "start_time": self._format_timestamp(start_time),
                "end_time": self._format_timestamp(end_time),
                "start_seconds": start_time,
                "end_seconds": end_time
            })

            current_time = end_time

        return timed_scenes

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds into MM:SS or HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    def create_complete_scene_plan(self, script: str, style: str = "cinematic horror") -> Dict[str, Any]:
        """Generate complete scene plan with images and animations"""
        print("🎬 Breaking down script into scenes...")
        breakdown = self.break_down_script(script)

        scenes = breakdown.get('scenes', [])

        print(f"🖼️  Generating image prompts for {len(scenes)} scenes...")
        image_prompts = self.generate_image_prompts(scenes, style)

        print("🎞️  Generating animation instructions...")
        animation_prompts = self.generate_animation_prompts(scenes)

        print("⏱️  Calculating precise timings...")
        timed_scenes = self.calculate_scene_timings(scenes)

        # Merge all data
        complete_scenes = []
        for i, scene in enumerate(timed_scenes):
            complete_scene = {
                **scene,
                "image_prompt": image_prompts[i].get('image_prompt', '') if i < len(image_prompts) else '',
                "full_image_prompt": image_prompts[i].get('full_prompt', '') if i < len(image_prompts) else '',
                "animation": animation_prompts[i] if i < len(animation_prompts) else {}
            }
            complete_scenes.append(complete_scene)

        return {
            "total_duration": breakdown.get('total_duration', 0),
            "scene_count": len(complete_scenes),
            "scenes": complete_scenes
        }

    def save_scenes_to_database(self, script_id: int, scenes: List[Dict[str, Any]]) -> None:
        """Save scene plan to database"""
        scene_data = []

        for scene in scenes:
            scene_data.append({
                "scene_number": scene.get('scene_number'),
                "content": scene.get('content', ''),
                "image_prompt": scene.get('image_prompt', ''),
                "animation_prompt": str(scene.get('animation', {})),
                "duration": scene.get('duration_seconds', 0)
            })

        self.db.save_scenes(script_id, scene_data)

    def generate_shot_list(self, scenes: List[Dict[str, Any]]) -> str:
        """Generate a detailed shot list for video production"""
        shot_list = "# VIDEO SHOT LIST\n\n"

        for scene in scenes:
            shot_list += f"## Scene {scene.get('scene_number')}: {scene.get('title', 'Untitled')}\n\n"
            shot_list += f"**Duration:** {scene.get('duration_seconds', 0)} seconds\n"
            shot_list += f"**Timing:** {scene.get('start_time', '0:00')} - {scene.get('end_time', '0:00')}\n\n"

            shot_list += f"**Narration:**\n{scene.get('content', '')}\n\n"

            shot_list += f"**Visual:**\n{scene.get('visual_description', '')}\n\n"

            shot_list += f"**Mood:** {scene.get('mood', '')}\n\n"

            if scene.get('image_prompt'):
                shot_list += f"**Image Prompt:**\n{scene.get('image_prompt', '')}\n\n"

            animation = scene.get('animation', {})
            if animation:
                shot_list += f"**Camera:** {animation.get('camera_movement', 'static')}\n"
                shot_list += f"**Motion:** {animation.get('subject_motion', 'none')}\n"
                shot_list += f"**Transition:** {animation.get('transition', 'cut')}\n\n"

            shot_list += "---\n\n"

        return shot_list

    def optimize_scene_pacing(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze and optimize scene pacing"""
        prompt = f"""Analyze the pacing of these scenes and suggest optimizations:

{str(scenes[:5])}... (showing first 5 scenes)

Total scenes: {len(scenes)}

Evaluate:
1. Are any scenes too long or too short?
2. Is there good variety in pacing?
3. Do slower moments balance intense moments?
4. Are transitions well-placed?

Return as JSON:
{{
    "overall_pacing": "assessment",
    "recommendations": [
        {{
            "scene_number": 3,
            "current_duration": 45,
            "suggested_duration": 30,
            "reason": "This scene drags; tighten it"
        }}
    ]
}}"""

        return self.client.generate_json_completion(prompt)

    def generate_b_roll_suggestions(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggest B-roll footage for each scene"""
        b_roll = []

        for scene in scenes[:5]:  # Sample first 5 scenes
            prompt = f"""Suggest B-roll footage options for this scene:

Scene: {scene.get('title')}
Content: {scene.get('content', '')[:200]}
Mood: {scene.get('mood', '')}

Suggest 3-5 B-roll shot ideas that could enhance this scene.

Return as JSON:
{{
    "b_roll_shots": [
        {{
            "description": "shot description",
            "purpose": "why this shot enhances the scene",
            "source": "stock footage / custom shoot / AI generated"
        }}
    ]
}}"""

            result = self.client.generate_json_completion(prompt)
            b_roll.append({
                "scene_number": scene.get('scene_number'),
                "b_roll_shots": result.get('b_roll_shots', [])
            })

        return b_roll
