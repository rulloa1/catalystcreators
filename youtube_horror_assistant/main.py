#!/usr/bin/env python3
"""
YouTube Horror Content Assistant
Main CLI Application

A comprehensive tool for creating horror content for YouTube
"""

import sys
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.config_manager import ConfigManager
from modules.database import ContentDatabase
from modules.openai_client import OpenAIClient
from modules.channel_setup import ChannelSetup
from modules.content_planning import ContentPlanner
from modules.script_generator import ScriptGenerator
from modules.metadata_generator import MetadataGenerator
from modules.scene_planner import ScenePlanner
from modules.exporter import ContentExporter
from modules.template_manager import TemplateManager


class HorrorAssistant:
    """Main application class for YouTube Horror Assistant"""

    def __init__(self):
        self.config = ConfigManager("config")
        self.validate_setup()

        # Initialize database
        db_path = self.config.get("paths.data_dir", "data") + "/horror_content.db"
        self.db = ContentDatabase(db_path)

        # Initialize OpenAI client
        api_key = self.config.get_openai_key()
        model = self.config.get("api.model", "gpt-4-turbo-preview")
        temperature = self.config.get("api.temperature", 0.7)
        max_tokens = self.config.get("api.max_tokens", 4000)

        self.openai = OpenAIClient(api_key, model, temperature, max_tokens)

        # Initialize modules
        self.channel_setup = ChannelSetup(self.openai)
        self.content_planner = ContentPlanner(self.openai, self.db)
        self.script_generator = ScriptGenerator(self.openai, self.db)
        self.metadata_generator = MetadataGenerator(self.openai, self.db)
        self.scene_planner = ScenePlanner(self.openai, self.db)

        exports_dir = self.config.get("paths.exports_dir", "exports")
        self.exporter = ContentExporter(exports_dir)

        templates_dir = self.config.get("paths.templates_dir", "templates")
        self.templates = TemplateManager(templates_dir)

        # Current session data
        self.current_project = {}

    def validate_setup(self):
        """Validate configuration and setup"""
        is_valid, errors = self.config.validate_config()

        if not is_valid:
            print("⚠️  Configuration Issues:")
            for error in errors:
                print(f"   - {error}")
            print()

            if not self.config.get_openai_key():
                print("To set your OpenAI API key:")
                print("1. Edit config/settings.json")
                print("2. OR set OPENAI_API_KEY environment variable")
                print()
                response = input("Would you like to set it now? (y/n): ")

                if response.lower() == 'y':
                    api_key = input("Enter your OpenAI API key: ").strip()
                    self.config.set("api.openai_api_key", api_key)
                    print("✅ API key saved!")
                else:
                    print("❌ Cannot proceed without API key.")
                    sys.exit(1)

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🎬 YOUTUBE HORROR CONTENT ASSISTANT")
        print("="*60)
        print()
        print("1. 📺 Setup New Channel")
        print("2. 💡 Generate Story Ideas")
        print("3. 📝 Create Script")
        print("4. 🎯 Generate Video Metadata")
        print("5. 🎬 Create Scene Breakdown")
        print("6. 📦 Complete Project Workflow")
        print("7. 📊 View Saved Content")
        print("8. 🔧 Settings")
        print("9. ❓ Help")
        print("0. 🚪 Exit")
        print()

    def run(self):
        """Run the main application loop"""
        print("\n👻 Welcome to YouTube Horror Content Assistant!\n")

        while True:
            self.display_menu()

            choice = input("Select an option (0-9): ").strip()

            if choice == '1':
                self.setup_channel()
            elif choice == '2':
                self.generate_story_ideas()
            elif choice == '3':
                self.create_script()
            elif choice == '4':
                self.generate_metadata()
            elif choice == '5':
                self.create_scene_breakdown()
            elif choice == '6':
                self.complete_workflow()
            elif choice == '7':
                self.view_saved_content()
            elif choice == '8':
                self.manage_settings()
            elif choice == '9':
                self.show_help()
            elif choice == '0':
                print("\n👋 Thanks for using Horror Content Assistant!")
                break
            else:
                print("❌ Invalid option. Please try again.")

    def setup_channel(self):
        """Channel setup workflow"""
        print("\n" + "="*60)
        print("📺 CHANNEL SETUP")
        print("="*60 + "\n")

        # Select niche
        print(self.templates.display_niche_options())
        niche_list = self.templates.get_niche_list()

        print(f"Available niches: {', '.join(niche_list)}")
        niche = input("\nEnter niche (or press Enter for 'paranormal'): ").strip() or "paranormal"

        if niche not in niche_list:
            print(f"⚠️  '{niche}' not found. Using 'paranormal'")
            niche = "paranormal"

        style = input("Enter style preference (or press Enter for 'mysterious'): ").strip() or "mysterious"
        target_audience = input("Target audience (or press Enter for 'horror enthusiasts'): ").strip() or "horror enthusiasts"

        preferences = {
            "niche": niche,
            "style": style,
            "target_audience": target_audience,
            "num_channel_names": 10
        }

        print("\n🎬 Generating channel package...")
        try:
            channel_data = self.channel_setup.create_complete_channel_package(preferences)

            print("\n✅ Channel package generated!\n")
            print(f"📺 Selected Name: {channel_data['selected_name']}")
            print(f"\n🎯 Alternative Names:")
            for i, name in enumerate(channel_data['channel_names'][:5], 1):
                print(f"   {i}. {name}")

            # Save to database
            self.db.save_channel(
                name=channel_data['selected_name'],
                description=channel_data['description']['full_description'],
                keywords=channel_data['keywords'],
                logo_prompt=channel_data['logo_prompts']['minimalist_prompt']
            )

            # Export
            export_files = self.exporter.export_to_markdown(
                channel_data,
                f"channel_{channel_data['selected_name'].replace(' ', '_')}",
                content_type="channel"
            )

            print(f"\n💾 Exported to: {export_files}")

            self.current_project['channel'] = channel_data

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        input("\nPress Enter to continue...")

    def generate_story_ideas(self):
        """Generate story ideas workflow"""
        print("\n" + "="*60)
        print("💡 STORY IDEAS GENERATION")
        print("="*60 + "\n")

        # Select niche
        niche_list = self.templates.get_niche_list()
        print(f"Available niches: {', '.join(niche_list)}")
        niche = input("\nEnter niche (default: paranormal): ").strip() or "paranormal"

        count = input("How many ideas? (default: 5): ").strip()
        count = int(count) if count.isdigit() else 5

        duration = input("Target duration in minutes? (default: 5): ").strip()
        duration = int(duration) if duration.isdigit() else 5

        print(f"\n💭 Generating {count} {niche} story ideas...")

        try:
            ideas = self.content_planner.generate_story_ideas(
                niche=niche,
                count=count,
                target_duration=duration,
                use_trends=True
            )

            print(f"\n✅ Generated {len(ideas)} ideas!\n")

            for i, idea in enumerate(ideas, 1):
                print(f"{i}. {idea.get('title', 'Untitled')}")
                print(f"   {idea.get('description', '')[:100]}...")
                print()

            # Save to database
            idea_ids = self.content_planner.save_ideas_to_database(ideas)
            print(f"💾 Saved to database (IDs: {idea_ids})")

            # Export
            export_file = self.exporter.export_to_markdown(
                {"ideas": ideas},
                f"story_ideas_{niche}",
                content_type="story_ideas"
            )

            print(f"📄 Exported to: {export_file}")

            self.current_project['story_ideas'] = ideas

            # Ask if user wants to select one
            select = input("\nSelect an idea to work with? (enter number or 'n'): ").strip()
            if select.isdigit() and 1 <= int(select) <= len(ideas):
                self.current_project['selected_idea'] = ideas[int(select) - 1]
                print(f"✅ Selected: {ideas[int(select) - 1].get('title')}")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        input("\nPress Enter to continue...")

    def create_script(self):
        """Script generation workflow"""
        print("\n" + "="*60)
        print("📝 SCRIPT GENERATION")
        print("="*60 + "\n")

        # Check if we have a selected idea
        if 'selected_idea' in self.current_project:
            idea = self.current_project['selected_idea']
            print(f"Using selected idea: {idea.get('title')}\n")
        else:
            print("No story idea selected. Using manual input...\n")
            title = input("Story title: ").strip()
            description = input("Story description: ").strip()
            hook = input("Opening hook: ").strip()
            niche = input("Niche: ").strip() or "horror"

            idea = {
                "title": title,
                "description": description,
                "hook": hook,
                "niche": niche
            }

        duration = input("Target duration in minutes (default: 5): ").strip()
        duration = int(duration) if duration.isdigit() else 5

        # Ask about reference transcript
        use_reference = input("\nDo you have a reference transcript to match style? (y/n): ").strip().lower()

        if use_reference == 'y':
            ref_path = input("Enter path to reference transcript file: ").strip()
            try:
                with open(ref_path, 'r', encoding='utf-8') as f:
                    reference = f.read()

                print("\n🔍 Analyzing reference style...")
                self.script_generator.analyze_reference_transcript(reference)
                print("✅ Style analysis complete!")

            except Exception as e:
                print(f"⚠️  Could not load reference: {e}")
                reference = None
        else:
            reference = None

        print(f"\n✍️  Generating {duration}-minute script...")

        try:
            script = self.script_generator.generate_script(
                story_idea=idea,
                target_duration=duration,
                use_reference_style=reference is not None
            )

            print("\n✅ Script generated!\n")
            print("Preview (first 500 characters):")
            print("-" * 60)
            print(script[:500] + "...")
            print("-" * 60)

            # Calculate timing
            timing = self.script_generator.estimate_reading_time(script)
            print(f"\n📊 Script Stats:")
            print(f"   Words: {timing['word_count']}")
            print(f"   Duration: {timing['formatted_duration']}")
            print(f"   WPM: {timing['words_per_minute']}")

            # Save to database
            script_id = self.script_generator.save_script_to_database(
                script=script,
                story_id=None,
                duration=duration,
                reference_transcript=reference
            )

            print(f"\n💾 Saved to database (ID: {script_id})")

            # Export
            export_data = {
                "script": script,
                "story_idea": idea,
                "timing": timing
            }

            export_file = self.exporter.export_to_markdown(
                export_data,
                f"script_{idea.get('title', 'untitled').replace(' ', '_')}",
                content_type="script"
            )

            print(f"📄 Exported to: {export_file}")

            self.current_project['script'] = script
            self.current_project['script_id'] = script_id
            self.current_project['timing'] = timing

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        input("\nPress Enter to continue...")

    def generate_metadata(self):
        """Metadata generation workflow"""
        print("\n" + "="*60)
        print("🎯 VIDEO METADATA GENERATION")
        print("="*60 + "\n")

        # Check if we have a script
        if 'script' not in self.current_project:
            print("⚠️  No script found. Please create a script first.")
            input("\nPress Enter to continue...")
            return

        script = self.current_project['script']
        idea = self.current_project.get('selected_idea', {})

        print("📋 Generating complete metadata package...")

        try:
            metadata = self.metadata_generator.generate_complete_metadata(
                script=script,
                story_idea=idea,
                channel_info=self.current_project.get('channel')
            )

            print("\n✅ Metadata generated!\n")

            print("📌 Title Options:")
            for i, title in enumerate(metadata['titles'], 1):
                print(f"   {i}. {title}")

            print(f"\n🏷️  Tags: {len(metadata['tags'])} tags generated")
            print(f"🖼️  Thumbnail Prompts: {len(metadata['thumbnail_prompts'])} options")

            # Save to database
            if 'script_id' in self.current_project:
                self.metadata_generator.save_metadata_to_database(
                    script_id=self.current_project['script_id'],
                    titles=metadata['titles'],
                    description=metadata['description'],
                    tags=metadata['tags'],
                    thumbnail_prompts=metadata['thumbnail_prompts']
                )

            # Export
            export_file = self.exporter.export_to_markdown(
                metadata,
                f"metadata_{idea.get('title', 'untitled').replace(' ', '_')}",
                content_type="metadata"
            )

            print(f"\n📄 Exported to: {export_file}")

            self.current_project['metadata'] = metadata

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        input("\nPress Enter to continue...")

    def create_scene_breakdown(self):
        """Scene breakdown workflow"""
        print("\n" + "="*60)
        print("🎬 SCENE BREAKDOWN")
        print("="*60 + "\n")

        # Check if we have a script
        if 'script' not in self.current_project:
            print("⚠️  No script found. Please create a script first.")
            input("\nPress Enter to continue...")
            return

        script = self.current_project['script']

        style = input("Visual style (default: cinematic horror): ").strip() or "cinematic horror"

        print("\n🎞️  Creating complete scene plan...")

        try:
            scene_plan = self.scene_planner.create_complete_scene_plan(
                script=script,
                style=style
            )

            print(f"\n✅ Scene plan created!")
            print(f"📊 Total scenes: {scene_plan['scene_count']}")
            print(f"⏱️  Total duration: {scene_plan['total_duration']:.1f} minutes\n")

            # Show first few scenes
            print("First 3 scenes:")
            for scene in scene_plan['scenes'][:3]:
                print(f"   Scene {scene['scene_number']}: {scene.get('title', 'Untitled')}")
                print(f"   Duration: {scene.get('duration_seconds', 0)}s")
                print()

            # Save to database
            if 'script_id' in self.current_project:
                self.scene_planner.save_scenes_to_database(
                    script_id=self.current_project['script_id'],
                    scenes=scene_plan['scenes']
                )

            # Export
            export_file = self.exporter.export_to_markdown(
                scene_plan,
                f"scenes_{self.current_project.get('selected_idea', {}).get('title', 'untitled').replace(' ', '_')}",
                content_type="scenes"
            )

            print(f"📄 Exported to: {export_file}")

            # Generate shot list
            shot_list = self.scene_planner.generate_shot_list(scene_plan['scenes'])
            shot_list_file = self.exporter.export_dir / f"shot_list_{self.current_project.get('selected_idea', {}).get('title', 'untitled').replace(' ', '_')}.md"

            with open(shot_list_file, 'w', encoding='utf-8') as f:
                f.write(shot_list)

            print(f"📋 Shot list exported to: {shot_list_file}")

            self.current_project['scenes'] = scene_plan

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

        input("\nPress Enter to continue...")

    def complete_workflow(self):
        """Complete workflow from idea to export"""
        print("\n" + "="*60)
        print("📦 COMPLETE PROJECT WORKFLOW")
        print("="*60 + "\n")

        print("This will guide you through the complete process:")
        print("1. Story idea")
        print("2. Script generation")
        print("3. Metadata creation")
        print("4. Scene breakdown")
        print("5. Complete export\n")

        proceed = input("Continue? (y/n): ").strip().lower()
        if proceed != 'y':
            return

        # Step 1: Story idea
        print("\n" + "="*60)
        print("STEP 1: Story Idea")
        print("="*60)
        self.generate_story_ideas()

        if 'selected_idea' not in self.current_project:
            print("⚠️  No idea selected. Workflow cancelled.")
            return

        # Step 2: Script
        print("\n" + "="*60)
        print("STEP 2: Script Generation")
        print("="*60)
        self.create_script()

        if 'script' not in self.current_project:
            print("⚠️  Script generation failed. Workflow cancelled.")
            return

        # Step 3: Metadata
        print("\n" + "="*60)
        print("STEP 3: Metadata Generation")
        print("="*60)
        self.generate_metadata()

        # Step 4: Scenes
        print("\n" + "="*60)
        print("STEP 4: Scene Breakdown")
        print("="*60)
        self.create_scene_breakdown()

        # Step 5: Complete export
        print("\n" + "="*60)
        print("STEP 5: Complete Export")
        print("="*60)

        project_name = self.current_project.get('selected_idea', {}).get('title', 'horror_video').replace(' ', '_')

        try:
            export_files = self.exporter.export_complete_project(
                self.current_project,
                project_name
            )

            print("\n✅ Complete project exported!")
            print("\n📁 Generated files:")
            for file_type, file_path in export_files.items():
                print(f"   {file_type}: {file_path}")

            # Create checklist
            checklist = self.metadata_generator.create_upload_checklist(
                self.current_project.get('metadata', {})
            )

            print("\n📋 Upload Checklist:")
            for item in checklist:
                print(f"   {item}")

        except Exception as e:
            print(f"\n❌ Error during export: {str(e)}")

        input("\nPress Enter to continue...")

    def view_saved_content(self):
        """View saved content from database"""
        print("\n" + "="*60)
        print("📊 SAVED CONTENT")
        print("="*60 + "\n")

        print("1. View story ideas")
        print("2. View scripts")
        print("3. Back")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            ideas = self.db.get_story_ideas(status="pending", limit=10)
            print(f"\n Found {len(ideas)} saved ideas:\n")

            for idea in ideas:
                print(f"ID: {idea['id']}")
                print(f"Title: {idea['title']}")
                print(f"Niche: {idea['niche']}")
                print(f"Created: {idea['created_at']}")
                print()

        elif choice == '2':
            print("(Script viewing functionality - would query database)")

        input("\nPress Enter to continue...")

    def manage_settings(self):
        """Manage application settings"""
        print("\n" + "="*60)
        print("🔧 SETTINGS")
        print("="*60 + "\n")

        print("Current configuration:\n")
        print(self.config.display_config())

        print("\n1. Update API key")
        print("2. Change model")
        print("3. View niche templates")
        print("4. Back")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            new_key = input("Enter new OpenAI API key: ").strip()
            self.config.set("api.openai_api_key", new_key)
            print("✅ API key updated!")

        elif choice == '2':
            print("\nAvailable models:")
            print("1. gpt-4-turbo-preview (recommended)")
            print("2. gpt-4")
            print("3. gpt-3.5-turbo (faster, cheaper)")

            model_choice = input("Select model: ").strip()
            models = {
                "1": "gpt-4-turbo-preview",
                "2": "gpt-4",
                "3": "gpt-3.5-turbo"
            }

            if model_choice in models:
                self.config.set("api.model", models[model_choice])
                print(f"✅ Model updated to {models[model_choice]}")

        elif choice == '3':
            print("\n" + self.templates.display_niche_options())

        input("\nPress Enter to continue...")

    def show_help(self):
        """Show help information"""
        print("\n" + "="*60)
        print("❓ HELP")
        print("="*60 + "\n")

        print("YouTube Horror Content Assistant")
        print("\nThis tool helps you create complete horror content for YouTube:")
        print()
        print("📺 Channel Setup: Generate channel names, descriptions, keywords")
        print("💡 Story Ideas: Generate viral horror story concepts")
        print("📝 Scripts: Create full scripts with style matching")
        print("🎯 Metadata: Generate titles, descriptions, tags, thumbnails")
        print("🎬 Scenes: Break down scripts into scenes with visuals")
        print("📦 Complete Workflow: Do everything in one flow")
        print()
        print("For more information, see the README.md file")
        print()
        print("Requirements:")
        print("- OpenAI API key (set in config/settings.json)")
        print("- Python 3.8+")
        print("- Required packages (see requirements.txt)")

        input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    try:
        app = HorrorAssistant()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
