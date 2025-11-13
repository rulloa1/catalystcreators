# 🚀 Quick Start Guide

Get up and running with YouTube Horror Content Assistant in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
cd youtube_horror_assistant
pip install -r requirements.txt
```

## Step 2: Configure API Key (2 minutes)

**Option A: Configuration File (Recommended)**
```bash
cp config/settings.example.json config/settings.json
```

Edit `config/settings.json` and replace `"sk-your-api-key-here"` with your actual OpenAI API key.

**Option B: Environment Variable**
```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

## Step 3: Run the Application (30 seconds)

```bash
python main.py
```

## Step 4: Create Your First Video (2 minutes)

1. Select option **6** (Complete Project Workflow)
2. Choose a horror niche (e.g., type `paranormal`)
3. Review generated story ideas
4. Select your favorite idea (e.g., type `1`)
5. Set script duration (e.g., type `5` for 5 minutes)
6. Answer `n` when asked about reference transcript
7. Wait for the complete generation process

**Done!** Check the `exports/` folder for all your generated files.

## What You'll Get

After the workflow completes, you'll have:

- ✅ **Complete Video Script** - Ready to record
- ✅ **5 Title Options** - Pick the most clickable
- ✅ **SEO Description** - Optimized for search
- ✅ **30+ Tags** - Maximize visibility
- ✅ **5 Thumbnail Prompts** - For image generation
- ✅ **Scene Breakdown** - With image prompts for each scene
- ✅ **Shot List** - Step-by-step production guide

## File Locations

Your generated content is saved in:
- `exports/*.json` - Machine-readable data
- `exports/*.md` - Human-readable documents
- `data/horror_content.db` - Saved ideas and scripts

## Next Steps

### Try Different Niches
- `paranormal` - Ghosts and hauntings
- `urban_legends` - Modern creepypastas
- `true_crime` - Mysterious cases
- `cryptids` - Unknown creatures
- `personal_experiences` - Real encounters

### Explore Individual Features
- **Option 1**: Setup channel (names, descriptions, logos)
- **Option 2**: Generate more story ideas
- **Option 3**: Create scripts with style matching
- **Option 4**: Generate metadata only
- **Option 5**: Create scene breakdowns

### Customize Your Style
1. Provide a reference transcript (Option 3)
2. The AI will analyze and match the style
3. All future scripts will follow that pattern

## Common Issues

**"Configuration Issues" error**
→ Make sure you've set your OpenAI API key in `config/settings.json`

**"OpenAI API error"**
→ Check that your API key is valid and you have credits

**"Module not found"**
→ Run `pip install -r requirements.txt` again

## Tips for Best Results

1. **Start with 5-minute scripts** - Easier to produce
2. **Generate multiple ideas** - Pick the best one
3. **Review and edit** - AI assists, you create
4. **Use reference transcripts** - For consistent style
5. **Save everything** - Ideas can be reused later

## Production Workflow

After generating content:

1. **Record Voice-Over** - Use the script
2. **Generate Images** - Use the image prompts
3. **Edit Video** - Follow the scene breakdown
4. **Create Thumbnail** - Use thumbnail prompts
5. **Upload** - Use the metadata (title, description, tags)
6. **Share** - Promote your video

## Get Help

- Read the full [README.md](README.md) for detailed documentation
- Check `templates/horror_niches.json` for niche details
- Review example exports in `exports/`

---

**Ready to create horror content? Run `python main.py` and let's go! 👻**
