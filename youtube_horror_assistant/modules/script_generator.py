"""
Script Generation Module for YouTube Horror Assistant
Analyzes reference transcripts and generates custom horror scripts
"""

from typing import Dict, Any, Optional
import re
from .openai_client import OpenAIClient
from .database import ContentDatabase


class ScriptGenerator:
    """Handles script generation with style matching"""

    def __init__(self, openai_client: OpenAIClient, database: ContentDatabase):
        self.client = openai_client
        self.db = database
        self.reference_style = None

    def analyze_reference_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze a reference transcript to understand style and structure"""
        print("🔍 Analyzing reference transcript style...")

        style_analysis = self.client.analyze_text_style(transcript)

        # Additional structural analysis
        word_count = len(transcript.split())
        estimated_duration = word_count / 150  # Assuming 150 words per minute

        structure_prompt = f"""Analyze this horror script's structure:

{transcript[:2000]}...

Identify:
1. How the hook is structured (first 30 seconds)
2. Story progression pattern
3. Use of suspense and pacing
4. How climax is built
5. Closing technique

Return as JSON:
{{
    "hook_structure": "description",
    "progression_pattern": "description",
    "suspense_techniques": ["technique1", "technique2"],
    "climax_approach": "description",
    "closing_style": "description",
    "word_count_per_minute": 150
}}"""

        structure_analysis = self.client.generate_json_completion(structure_prompt)

        # Combine analyses
        complete_analysis = {
            **style_analysis,
            **structure_analysis,
            "word_count": word_count,
            "estimated_duration_minutes": round(estimated_duration, 1)
        }

        self.reference_style = complete_analysis
        return complete_analysis

    def generate_script(self, story_idea: Dict[str, Any], target_duration: int = 5, use_reference_style: bool = True) -> str:
        """Generate a complete horror script"""
        target_word_count = target_duration * 150  # 150 words per minute

        style_instructions = ""
        if use_reference_style and self.reference_style:
            style_instructions = f"""
Match this writing style:
- Tone: {self.reference_style.get('tone', 'engaging')}
- Pacing: {self.reference_style.get('pacing', 'moderate')}
- Hook structure: {self.reference_style.get('hook_structure', 'standard')}
- Suspense techniques: {', '.join(self.reference_style.get('suspense_techniques', []))}
- Narrative perspective: {self.reference_style.get('narrative_perspective', 'third person')}
"""

        prompt = f"""Write a complete YouTube horror script based on this story idea:

Title: {story_idea.get('title')}
Description: {story_idea.get('description')}
Hook: {story_idea.get('hook')}

Target duration: {target_duration} minutes (approximately {target_word_count} words)

{style_instructions}

Requirements:
1. Start with a powerful hook in the first 30 seconds
2. Build suspense gradually
3. Include vivid, atmospheric descriptions
4. Create emotional engagement
5. Build to a satisfying climax
6. End with impact (twist, revelation, or lingering fear)
7. Natural, conversational delivery suitable for voice-over
8. Clear scene transitions

Format the script with:
- [HOOK] marker at the beginning
- [SCENE X] markers for major transitions
- [CLIMAX] marker at the peak moment
- [OUTRO] marker for the closing

Write the complete script now."""

        script = self.client.generate_completion(
            prompt,
            temperature=0.8,
            max_tokens=target_word_count * 2  # Allow for longer generation
        )

        return script

    def generate_script_with_outline(self, outline: Dict[str, Any], target_duration: int = 5) -> str:
        """Generate script from a detailed outline"""
        target_word_count = target_duration * 150

        prompt = f"""Write a complete horror script based on this detailed outline:

Act Structure:
Act 1: {outline.get('act_structure', {}).get('act1', '')}
Act 2: {outline.get('act_structure', {}).get('act2', '')}
Act 3: {outline.get('act_structure', {}).get('act3', '')}

Key Beats: {', '.join(outline.get('key_beats', []))}

Atmosphere: {outline.get('atmosphere', '')}

Visual Elements: {', '.join(outline.get('visual_elements', []))}

Target: {target_word_count} words ({target_duration} minutes)

Write a complete, engaging horror script that follows this outline. Include scene markers and maintain consistent pacing."""

        return self.client.generate_completion(prompt, temperature=0.8)

    def refine_script(self, script: str, feedback: str) -> str:
        """Refine a script based on user feedback"""
        prompt = f"""Refine this horror script based on the following feedback:

Original Script:
{script}

Feedback: {feedback}

Provide the complete refined script, maintaining the overall structure but addressing the feedback."""

        return self.client.generate_completion(prompt, temperature=0.7)

    def adjust_script_length(self, script: str, target_duration: int) -> str:
        """Adjust script length to match target duration"""
        current_word_count = len(script.split())
        current_duration = current_word_count / 150
        target_word_count = target_duration * 150

        if abs(current_duration - target_duration) < 0.5:
            return script  # Close enough

        action = "expand" if target_duration > current_duration else "condense"

        prompt = f"""{"Expand" if action == "expand" else "Condense"} this horror script to approximately {target_word_count} words ({target_duration} minutes).

Current script ({current_word_count} words):
{script}

Requirements:
- Maintain the core story and impact
- Keep the hook and climax strong
- {"Add more atmospheric details and build more suspense" if action == "expand" else "Tighten the pacing while keeping key moments"}
- Preserve scene markers and structure

Provide the complete adjusted script."""

        return self.client.generate_completion(prompt, temperature=0.7, max_tokens=target_word_count * 2)

    def add_sound_cues(self, script: str) -> str:
        """Add sound effect and music cues to script"""
        prompt = f"""Add sound effect and music cues to this horror script:

{script}

Add cues in [BRACKETS] like:
- [SFX: specific sound effect]
- [MUSIC: mood/style description]
- [AMBIENT: background sounds]

Place cues strategically to enhance atmosphere and impact. Don't overdo it - only where it adds value.

Return the script with sound cues added."""

        return self.client.generate_completion(prompt, temperature=0.6)

    def generate_multiple_versions(self, story_idea: Dict[str, Any], num_versions: int = 3) -> list[str]:
        """Generate multiple script variations"""
        scripts = []

        variations = [
            {"tone": "mysterious and slow-burn", "temp": 0.7},
            {"tone": "intense and fast-paced", "temp": 0.8},
            {"tone": "atmospheric and descriptive", "temp": 0.75}
        ]

        for i, variation in enumerate(variations[:num_versions]):
            print(f"Generating variation {i+1}/{num_versions}...")

            modified_idea = story_idea.copy()
            modified_idea['description'] = f"{modified_idea.get('description', '')} [Style: {variation['tone']}]"

            script = self.generate_script(modified_idea, use_reference_style=False)
            scripts.append({
                "version": i + 1,
                "style": variation['tone'],
                "script": script
            })

        return scripts

    def save_script_to_database(self, script: str, story_id: Optional[int], duration: int, reference_transcript: Optional[str] = None) -> int:
        """Save generated script to database"""
        return self.db.save_script(
            story_id=story_id,
            content=script,
            duration=duration,
            reference_transcript=reference_transcript
        )

    def estimate_reading_time(self, script: str, words_per_minute: int = 150) -> Dict[str, Any]:
        """Estimate how long it will take to read the script"""
        # Remove scene markers and other annotations
        clean_text = re.sub(r'\[.*?\]', '', script)
        word_count = len(clean_text.split())

        duration_minutes = word_count / words_per_minute
        duration_seconds = duration_minutes * 60

        return {
            "word_count": word_count,
            "duration_minutes": round(duration_minutes, 2),
            "duration_seconds": round(duration_seconds),
            "words_per_minute": words_per_minute,
            "formatted_duration": f"{int(duration_minutes)}:{int((duration_minutes % 1) * 60):02d}"
        }

    def extract_script_sections(self, script: str) -> Dict[str, str]:
        """Extract different sections from a script"""
        sections = {
            "hook": "",
            "main_content": "",
            "climax": "",
            "outro": ""
        }

        # Extract hook
        hook_match = re.search(r'\[HOOK\](.*?)(?:\[SCENE|\[CLIMAX|\[OUTRO|$)', script, re.DOTALL)
        if hook_match:
            sections["hook"] = hook_match.group(1).strip()

        # Extract climax
        climax_match = re.search(r'\[CLIMAX\](.*?)(?:\[OUTRO|\[SCENE|$)', script, re.DOTALL)
        if climax_match:
            sections["climax"] = climax_match.group(1).strip()

        # Extract outro
        outro_match = re.search(r'\[OUTRO\](.*?)$', script, re.DOTALL)
        if outro_match:
            sections["outro"] = outro_match.group(1).strip()

        # Main content is everything between hook and climax
        main_match = re.search(r'\[HOOK\].*?(\[SCENE.*?)(?:\[CLIMAX|$)', script, re.DOTALL)
        if main_match:
            sections["main_content"] = main_match.group(1).strip()

        return sections
