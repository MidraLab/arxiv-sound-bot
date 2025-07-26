# ArXiv Sound Bot Setup Guide

This bot monitors ArXiv for new papers in audio and speech processing categories and sends notifications to Discord.

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Discord webhook URL
- Google Gemini API key

## Installation Steps

### 1. Clone the repository
```bash
git clone <repository-url>
cd arxiv-sound-bot
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:
- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL
- `GEMINI_API_KEY`: Your Google Gemini API key

### 4. Test the setup
```bash
uv run python source/fetch_arxiv_papers.py
```

## What the bot does

1. **Searches ArXiv** for papers in these categories:
   - `eess.AS`: Audio and Speech Processing
   - `cs.SD`: Sound
   - `cs.CL`: Computation and Language (filtered for speech/voice/audio)

2. **Filters papers** by date (only processes papers from the last 7 days)

3. **Translates abstracts** to Japanese using Google Gemini

4. **Sends to Discord** with formatted messages including:
   - Paper title
   - Japanese translation of the abstract
   - Links to AlphaXiv, PDF, and ArXiv
   - Categories and publication date

5. **Tracks processed papers** to avoid duplicates using `opt/contents_info.json`

## Running the bot

### Manual execution
```bash
uv run python source/fetch_arxiv_papers.py
```

### Scheduled execution (recommended)
Set up a cron job or scheduled task to run the bot periodically (e.g., daily):
```bash
0 9 * * * cd /path/to/arxiv-sound-bot && uv run python source/fetch_arxiv_papers.py
```

## Troubleshooting

### API key error
If you see "API key not valid" error, ensure:
1. Your `.env` file contains valid credentials
2. The Gemini API key has proper permissions
3. The Discord webhook URL is correct

### No papers found
The bot only processes papers from the last 7 days. If no new papers match the search criteria, no messages will be sent.

### Environment variables not loaded
Make sure the `.env` file is in the project root directory and contains the required variables.

## Note on initialization issue

Currently, the bot initializes the Gemini API client even when environment variables are not set, which causes an error. To run without credentials, you would need to modify the code to lazy-load the Gemini client only when needed.