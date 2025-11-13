"""
Export Module for YouTube Horror Assistant
Handles exporting content to various formats (JSON, Markdown)
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ContentExporter:
    """Handles exporting content to different formats"""

    def __init__(self, export_dir: str = "exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_to_json(self, data: Dict[str, Any], filename: str) -> str:
        """Export data to JSON file"""
        filepath = self.export_dir / f"{filename}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def export_to_markdown(self, data: Dict[str, Any], filename: str, content_type: str = "general") -> str:
        """Export data to Markdown file"""
        filepath = self.export_dir / f"{filename}.md"

        if content_type == "channel":
            markdown = self._format_channel_markdown(data)
        elif content_type == "story_ideas":
            markdown = self._format_story_ideas_markdown(data)
        elif content_type == "script":
            markdown = self._format_script_markdown(data)
        elif content_type == "metadata":
            markdown = self._format_metadata_markdown(data)
        elif content_type == "scenes":
            markdown = self._format_scenes_markdown(data)
        elif content_type == "complete_project":
            markdown = self._format_complete_project_markdown(data)
        else:
            markdown = self._format_general_markdown(data)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)

        return str(filepath)

    def _format_channel_markdown(self, data: Dict[str, Any]) -> str:
        """Format channel setup data as markdown"""
        md = f"# YouTube Channel Setup\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        md += f"## Selected Channel Name\n\n**{data.get('selected_name', 'N/A')}**\n\n"

        md += f"## Channel Name Options\n\n"
        for i, name in enumerate(data.get('channel_names', []), 1):
            md += f"{i}. {name}\n"

        md += f"\n## Channel Description\n\n"
        desc = data.get('description', {})
        md += f"### Short Description\n\n{desc.get('short_description', '')}\n\n"
        md += f"### Full Description\n\n{desc.get('full_description', '')}\n\n"
        md += f"### About Section\n\n{desc.get('about_section', '')}\n\n"

        md += f"## SEO Keywords\n\n"
        for keyword in data.get('keywords', [])[:20]:  # First 20 keywords
            md += f"- {keyword}\n"

        md += f"\n## Logo Prompts\n\n"
        logo = data.get('logo_prompts', {})
        md += f"### Minimalist Style\n```\n{logo.get('minimalist_prompt', '')}\n```\n\n"
        md += f"### Detailed Style\n```\n{logo.get('detailed_prompt', '')}\n```\n\n"
        md += f"### Text-Focused Style\n```\n{logo.get('text_focused_prompt', '')}\n```\n\n"

        return md

    def _format_story_ideas_markdown(self, data: Dict[str, Any]) -> str:
        """Format story ideas as markdown"""
        md = f"# Horror Story Ideas\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        ideas = data.get('ideas', []) if isinstance(data, dict) else data

        for i, idea in enumerate(ideas, 1):
            md += f"## Idea {i}: {idea.get('title', 'Untitled')}\n\n"
            md += f"**Niche:** {idea.get('niche', 'N/A')}\n\n"
            md += f"**Target Duration:** {idea.get('estimated_duration', 5)} minutes\n\n"
            md += f"### Hook\n\n{idea.get('hook', '')}\n\n"
            md += f"### Description\n\n{idea.get('description', '')}\n\n"
            md += f"### Viral Potential\n\n{idea.get('viral_potential', '')}\n\n"
            md += f"### Target Audience\n\n{idea.get('target_audience', '')}\n\n"
            md += "---\n\n"

        return md

    def _format_script_markdown(self, data: Dict[str, Any]) -> str:
        """Format script as markdown"""
        md = f"# Horror Video Script\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        if 'story_idea' in data:
            idea = data['story_idea']
            md += f"## Story Information\n\n"
            md += f"**Title:** {idea.get('title', 'N/A')}\n\n"
            md += f"**Niche:** {idea.get('niche', 'N/A')}\n\n"

        if 'timing' in data:
            timing = data['timing']
            md += f"## Script Timing\n\n"
            md += f"- **Word Count:** {timing.get('word_count', 0)}\n"
            md += f"- **Duration:** {timing.get('formatted_duration', '0:00')}\n"
            md += f"- **Words Per Minute:** {timing.get('words_per_minute', 150)}\n\n"

        md += f"## Full Script\n\n"
        md += data.get('script', 'No script content')
        md += "\n\n"

        return md

    def _format_metadata_markdown(self, data: Dict[str, Any]) -> str:
        """Format video metadata as markdown"""
        md = f"# Video Metadata\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        md += f"## Title Options\n\n"
        for i, title in enumerate(data.get('titles', []), 1):
            md += f"{i}. {title}\n"

        md += f"\n## Video Description\n\n```\n{data.get('description', '')}\n```\n\n"

        md += f"## Tags\n\n"
        tags = data.get('tags', [])
        md += ", ".join(tags)
        md += "\n\n"

        md += f"## Thumbnail Prompts\n\n"
        for i, prompt in enumerate(data.get('thumbnail_prompts', []), 1):
            if isinstance(prompt, dict):
                md += f"### Option {i}\n\n"
                md += f"**Style:** {prompt.get('style', 'N/A')}\n\n"
                md += f"**Prompt:**\n```\n{prompt.get('prompt', '')}\n```\n\n"
                md += f"**Text Overlay:** {prompt.get('text_overlay', 'None')}\n\n"
            else:
                md += f"### Option {i}\n\n```\n{prompt}\n```\n\n"

        return md

    def _format_scenes_markdown(self, data: Dict[str, Any]) -> str:
        """Format scene plan as markdown"""
        md = f"# Scene Breakdown\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        md += f"**Total Duration:** {data.get('total_duration', 0):.1f} minutes\n\n"
        md += f"**Scene Count:** {data.get('scene_count', 0)}\n\n"

        md += "---\n\n"

        for scene in data.get('scenes', []):
            md += f"## Scene {scene.get('scene_number')}: {scene.get('title', 'Untitled')}\n\n"

            if 'start_time' in scene:
                md += f"**Timing:** {scene.get('start_time')} - {scene.get('end_time')} "
                md += f"({scene.get('duration_seconds', 0)}s)\n\n"

            md += f"**Mood:** {scene.get('mood', 'N/A')}\n\n"

            md += f"### Content\n\n{scene.get('content', '')}\n\n"

            md += f"### Visual Description\n\n{scene.get('visual_description', '')}\n\n"

            if scene.get('image_prompt'):
                md += f"### Image Generation Prompt\n\n```\n{scene.get('image_prompt', '')}\n```\n\n"

            animation = scene.get('animation', {})
            if animation:
                md += f"### Animation Instructions\n\n"
                md += f"- **Camera:** {animation.get('camera_movement', 'static')}\n"
                md += f"- **Motion:** {animation.get('subject_motion', 'none')}\n"
                md += f"- **Transition:** {animation.get('transition', 'cut')}\n\n"

            md += "---\n\n"

        return md

    def _format_complete_project_markdown(self, data: Dict[str, Any]) -> str:
        """Format complete project as comprehensive markdown"""
        md = f"# Complete Horror Video Project\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Table of Contents
        md += "## Table of Contents\n\n"
        md += "1. [Story Idea](#story-idea)\n"
        md += "2. [Script](#script)\n"
        md += "3. [Video Metadata](#video-metadata)\n"
        md += "4. [Scene Breakdown](#scene-breakdown)\n"
        md += "5. [Production Checklist](#production-checklist)\n\n"

        md += "---\n\n"

        # Story Idea
        if 'story_idea' in data:
            idea = data['story_idea']
            md += "## Story Idea\n\n"
            md += f"**Title:** {idea.get('title', 'N/A')}\n\n"
            md += f"**Niche:** {idea.get('niche', 'N/A')}\n\n"
            md += f"**Description:** {idea.get('description', '')}\n\n"
            md += f"**Hook:** {idea.get('hook', '')}\n\n"

        # Script
        if 'script' in data:
            md += "## Script\n\n"
            md += data['script']
            md += "\n\n"

        # Metadata
        if 'metadata' in data:
            metadata = data['metadata']
            md += "## Video Metadata\n\n"
            md += f"### Titles\n\n"
            for i, title in enumerate(metadata.get('titles', []), 1):
                md += f"{i}. {title}\n"
            md += "\n"

            md += f"### Description\n\n```\n{metadata.get('description', '')}\n```\n\n"

            md += f"### Tags\n\n{', '.join(metadata.get('tags', []))}\n\n"

        # Scenes
        if 'scenes' in data:
            md += "## Scene Breakdown\n\n"
            for scene in data['scenes'].get('scenes', []):
                md += f"### Scene {scene.get('scene_number')}\n\n"
                md += f"**{scene.get('title', 'Untitled')}** - "
                md += f"{scene.get('start_time', '0:00')} to {scene.get('end_time', '0:00')}\n\n"

        # Production Checklist
        md += "## Production Checklist\n\n"
        md += "### Pre-Production\n"
        md += "- [ ] Script finalized\n"
        md += "- [ ] Scene images generated\n"
        md += "- [ ] Voice-over recorded\n"
        md += "- [ ] Background music selected\n"
        md += "- [ ] Sound effects prepared\n\n"

        md += "### Production\n"
        md += "- [ ] All scenes created\n"
        md += "- [ ] Animations applied\n"
        md += "- [ ] Transitions added\n"
        md += "- [ ] Audio synced\n\n"

        md += "### Post-Production\n"
        md += "- [ ] Video edited\n"
        md += "- [ ] Thumbnail created\n"
        md += "- [ ] Metadata prepared\n"
        md += "- [ ] Video exported\n"
        md += "- [ ] Uploaded to YouTube\n\n"

        return md

    def _format_general_markdown(self, data: Dict[str, Any]) -> str:
        """Format general data as markdown"""
        md = f"# Content Export\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += "```json\n"
        md += json.dumps(data, indent=2, ensure_ascii=False)
        md += "\n```\n"
        return md

    def export_complete_project(self, project_data: Dict[str, Any], project_name: str) -> Dict[str, str]:
        """Export complete project in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"{project_name}_{timestamp}"

        exports = {}

        # Export as JSON
        json_file = self.export_to_json(project_data, base_filename)
        exports['json'] = json_file

        # Export as comprehensive Markdown
        md_file = self.export_to_markdown(project_data, base_filename, content_type="complete_project")
        exports['markdown'] = md_file

        # Export individual components
        if 'script' in project_data:
            script_file = self.export_to_markdown(
                {'script': project_data['script'], 'story_idea': project_data.get('story_idea'), 'timing': project_data.get('timing')},
                f"{base_filename}_script",
                content_type="script"
            )
            exports['script'] = script_file

        if 'metadata' in project_data:
            metadata_file = self.export_to_markdown(
                project_data['metadata'],
                f"{base_filename}_metadata",
                content_type="metadata"
            )
            exports['metadata'] = metadata_file

        if 'scenes' in project_data:
            scenes_file = self.export_to_markdown(
                project_data['scenes'],
                f"{base_filename}_scenes",
                content_type="scenes"
            )
            exports['scenes'] = scenes_file

        return exports

    def create_project_folder(self, project_name: str) -> Path:
        """Create a dedicated folder for a project"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_folder = self.export_dir / f"{project_name}_{timestamp}"
        project_folder.mkdir(parents=True, exist_ok=True)
        return project_folder
