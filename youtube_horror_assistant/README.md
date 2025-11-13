# 👻 YouTube Horror Content Assistant

A comprehensive Python-based tool for creating professional horror content for YouTube. This assistant helps you generate everything from channel setup to complete video production materials using AI.

## 🎬 Features

### Core Functionality

#### 1. **Channel Setup Module**
- Generate 10 unique horror channel name options
- Create SEO-optimized channel descriptions
- Generate trending keywords for maximum visibility
- Create text-to-image prompts for professional channel logos

#### 2. **Content Planning Module**
- Generate viral horror story ideas (5+ at a time)
- Support for 8 different horror sub-niches
- User selection and idea refinement
- Local database storage for future reference
- Content calendar planning

#### 3. **Script Generation Module**
- Analyze reference transcripts to match existing style
- Generate custom horror scripts (3-10+ minutes)
- Maintain natural, engaging storytelling
- Automatic hook placement and climax building
- Support for multiple script variations

#### 4. **Video Metadata Generator**
- Create 5 clickable title options per video
- Generate SEO-optimized descriptions
- Produce comprehensive tag lists
- Create text-to-image prompts for thumbnails
- Generate video timestamps

#### 5. **Scene Planning Tool**
- Break scripts into timed scenes
- Generate image prompts for each scene
- Create animation/motion instructions
- Calculate precise scene durations
- Produce shot lists for video production

## 📋 Horror Sub-Niches Supported

1. **Paranormal** - Ghosts, hauntings, supernatural encounters
2. **Urban Legends** - Modern myths, creepypastas, internet horror
3. **True Crime Horror** - Real mysterious cases with horror elements
4. **Cryptids** - Mysterious creatures, bigfoot, unknown animals
5. **Personal Experiences** - First-person real-life scary encounters
6. **Cosmic Horror** - Lovecraftian, existential dread
7. **Historical Horror** - Historical events with horror elements
8. **Psychological Horror** - Mind games, reality distortion

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection

### Installation

1. **Clone or download this repository**

```bash
cd youtube_horror_assistant
```

2. **Install required packages**

```bash
pip install -r requirements.txt
```

3. **Configure your API key**

Option A: Edit configuration file
```bash
cp config/settings.example.json config/settings.json
# Edit config/settings.json and add your OpenAI API key
```

Option B: Use environment variable
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"
```

4. **Run the application**

```bash
python main.py
```

## 📖 Usage Guide

### Main Menu Options

When you launch the application, you'll see:

```
🎬 YOUTUBE HORROR CONTENT ASSISTANT
==================================================

1. 📺 Setup New Channel
2. 💡 Generate Story Ideas
3. 📝 Create Script
4. 🎯 Generate Video Metadata
5. 🎬 Create Scene Breakdown
6. 📦 Complete Project Workflow
7. 📊 View Saved Content
8. 🔧 Settings
9. ❓ Help
0. 🚪 Exit
```

### Workflow Examples

#### Option 1: Complete Workflow (Recommended for beginners)

Select option **6** for a guided experience that:
1. Generates story ideas and lets you select one
2. Creates a complete script based on your selection
3. Generates all video metadata
4. Creates scene breakdown with visual prompts
5. Exports everything to organized files

#### Option 2: Step-by-Step (For customization)

**Step 1: Setup Channel**
- Select niche (e.g., "paranormal")
- Choose style preference (e.g., "mysterious")
- Review generated channel names and descriptions
- Exports to `exports/channel_*.md`

**Step 2: Generate Story Ideas**
- Select niche
- Choose number of ideas (default: 5)
- Set target duration (default: 5 minutes)
- Review and select your favorite idea
- Exports to `exports/story_ideas_*.md`

**Step 3: Create Script**
- Uses selected idea (or manual input)
- Optional: Provide reference transcript for style matching
- Set target duration
- Reviews generated script with statistics
- Exports to `exports/script_*.md`

**Step 4: Generate Metadata**
- Creates 5 title options
- Generates SEO description
- Produces 30-40 relevant tags
- Creates 5 thumbnail prompts
- Exports to `exports/metadata_*.md`

**Step 5: Scene Breakdown**
- Breaks script into scenes
- Generates image prompts for each scene
- Creates animation instructions
- Calculates precise timings
- Produces shot list
- Exports to `exports/scenes_*.md`

## 📁 Project Structure

```
youtube_horror_assistant/
├── main.py                 # Main CLI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── .env.example           # Environment variables template
│
├── modules/               # Core modules
│   ├── __init__.py
│   ├── config_manager.py      # Configuration management
│   ├── database.py            # SQLite database operations
│   ├── openai_client.py       # OpenAI API wrapper
│   ├── channel_setup.py       # Channel setup functionality
│   ├── content_planning.py    # Story idea generation
│   ├── script_generator.py    # Script creation
│   ├── metadata_generator.py  # Video metadata creation
│   ├── scene_planner.py       # Scene breakdown
│   ├── exporter.py            # Export to JSON/Markdown
│   └── template_manager.py    # Niche template management
│
├── config/                # Configuration files
│   ├── settings.json      # Main configuration (create from example)
│   └── settings.example.json  # Configuration template
│
├── templates/             # Horror niche templates
│   └── horror_niches.json     # Sub-niche definitions
│
├── data/                  # Database storage
│   └── horror_content.db      # SQLite database (auto-created)
│
└── exports/               # Generated content exports
    ├── *.json             # JSON exports
    ├── *.md               # Markdown exports
    └── shot_list_*.md     # Video production shot lists
```

## 🔧 Configuration

### API Settings

Edit `config/settings.json`:

```json
{
  "api": {
    "openai_api_key": "sk-your-key-here",
    "model": "gpt-4-turbo-preview",
    "temperature": 0.7,
    "max_tokens": 4000
  }
}
```

**Model Options:**
- `gpt-4-turbo-preview` - Recommended (best quality)
- `gpt-4` - High quality
- `gpt-3.5-turbo` - Faster, cheaper (lower quality)

**Temperature:** Controls creativity (0.0 = deterministic, 1.0 = very creative)

### Default Preferences

```json
{
  "defaults": {
    "horror_niche": "paranormal",
    "script_duration": 5,
    "num_title_options": 5,
    "num_channel_names": 10
  }
}
```

## 📤 Export Formats

### JSON Exports
Complete structured data in JSON format for programmatic access.

```json
{
  "story_idea": {...},
  "script": "...",
  "metadata": {...},
  "scenes": {...}
}
```

### Markdown Exports
Human-readable formatted documents:
- Channel setup details
- Story ideas with descriptions
- Complete scripts with timing
- Metadata with titles and tags
- Scene breakdowns with prompts
- Production shot lists

## 💡 Best Practices

### For Channel Setup
1. Generate multiple name options before deciding
2. Research existing channels to avoid name conflicts
3. Keep descriptions under 1000 characters
4. Use provided keywords but customize for your brand

### For Story Ideas
1. Generate 5-10 ideas at once for variety
2. Save ideas to database even if not using immediately
3. Refine selected ideas before scripting
4. Consider trending topics and seasonality

### For Scripts
1. Always use a reference transcript if you have one
2. Start with 5-minute scripts until comfortable
3. Review and edit generated scripts
4. Test reading speed (aim for 150 words/minute)

### For Metadata
1. Test multiple title options with target audience
2. Customize descriptions with personal touches
3. Add relevant hashtags to descriptions
4. Generate multiple thumbnail options

### For Scene Planning
1. Keep scenes between 15-45 seconds
2. Vary visual styles to maintain interest
3. Review all image prompts before generating images
4. Adjust scene timing based on content density

## 🔍 Advanced Features

### Reference Transcript Analysis
The assistant can analyze your favorite videos to match their style:

```python
# In script generation workflow
use_reference = input("Do you have a reference transcript? (y/n): ")
# Provide path to text file
# Style analysis is performed automatically
```

### Batch Processing
Generate multiple ideas across different niches:

```python
# Through the API (for developers)
results = content_planner.batch_generate_ideas(
    niches=["paranormal", "urban_legends", "true_crime"],
    count_per_niche=3
)
```

### Custom Niche Creation
Add your own horror sub-niches through the template manager.

### Analytics Tracking
Store performance metrics for generated content:

```python
content_planner.analyze_idea_performance(
    idea_id=1,
    metrics={"views": 10000, "ctr": 8.5}
)
```

## 🐛 Troubleshooting

### "OpenAI API error"
- Check your API key is valid
- Verify you have credits in your OpenAI account
- Check internet connection

### "Configuration Issues"
- Ensure `config/settings.json` exists
- Verify JSON format is valid
- Check all required fields are present

### "Database error"
- Ensure `data/` directory exists
- Check file permissions
- Delete database file to reset (loses saved content)

### "Module not found"
- Run `pip install -r requirements.txt`
- Ensure you're in the correct directory
- Check Python version (3.8+ required)

## 📊 Database Schema

The application uses SQLite to store:
- **Channels** - Channel setup information
- **Story Ideas** - Generated story concepts
- **Scripts** - Complete video scripts
- **Video Metadata** - Titles, descriptions, tags
- **Scenes** - Scene breakdowns with prompts
- **Analytics** - Performance tracking data

## 🔐 Security Notes

- **Never commit** `config/settings.json` with real API keys
- Use `.env` for sensitive configuration
- API keys are masked in settings display
- Database contains no sensitive data

## 📈 Roadmap / Future Features

- [ ] GUI interface (Tkinter or web-based)
- [ ] Integration with image generation APIs
- [ ] Voice synthesis integration
- [ ] Video editing automation
- [ ] YouTube API integration for direct upload
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Collaboration features
- [ ] Template marketplace

## 🤝 Contributing

This is a comprehensive tool that can be extended in many ways:
- Add new horror sub-niches
- Improve prompt templates
- Enhance export formats
- Add new AI models
- Create GUI interfaces

## 📜 License

See LICENSE file for details.

## ⚠️ Disclaimer

This tool uses AI to generate content. Always:
- Review and edit generated content
- Ensure content meets YouTube's guidelines
- Respect copyright and attribution
- Add your own creativity and personality
- Verify facts in "true" story content

## 💬 Support

For issues, questions, or suggestions:
1. Check this README thoroughly
2. Review example outputs in `exports/`
3. Consult horror niche templates
4. Check OpenAI API documentation

## 🎯 Tips for Success

1. **Start Simple** - Use the complete workflow first
2. **Iterate** - Generate multiple versions and pick the best
3. **Customize** - Always add your personal touch
4. **Test** - Try different niches to find your strength
5. **Analyze** - Track what works and refine your approach
6. **Be Consistent** - Develop a recognizable style
7. **Stay Authentic** - AI assists, but your voice matters most

## 📞 Getting Started Checklist

- [ ] Python 3.8+ installed
- [ ] OpenAI API key obtained
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Configuration file created (`config/settings.json`)
- [ ] API key configured
- [ ] Application runs successfully (`python main.py`)
- [ ] First channel setup completed
- [ ] First story idea generated
- [ ] First script created
- [ ] Understanding of export formats
- [ ] Comfortable with complete workflow

---

**Happy Horror Content Creating! 👻🎬**

*May your stories be terrifying, your thumbnails clickable, and your analytics growing!*
