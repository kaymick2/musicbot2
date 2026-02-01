# Spotify to YouTube Music Downloader

This tool allows you to automatically download your Spotify liked songs from YouTube using the Spotify API and yt-dlp.

## Prerequisites

- Python 3.6 or higher
- A Spotify Developer account and app (already configured with the provided credentials)
- Internet connection

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure yt-dlp is properly installed and accessible from your command line.

## Usage

### Step 1: Get your Spotify liked songs

Run the main script to fetch your liked songs from Spotify and then download them:

```bash
python main.py
```

The first time you run this, a browser window will open asking you to authorize the application with your Spotify account. After authorization, the script will:

1. Retrieve all your liked songs from Spotify
2. Save them to `liked_songs.txt` and `liked_songs.json`
3. Download each song from YouTube as MP3

### Download only (skip Spotify API)

If you've already retrieved your liked songs and just want to download them:

```bash
python main.py --download-only
```

### Change download directory

```bash
python main.py --output-dir "my_music_folder"
```

## Files

- `spotify_liked_songs.py`: Script to retrieve liked songs from Spotify
- `download_songs.py`: Script to download songs from YouTube
- `main.py`: Main script that combines both functionalities
- `liked_songs.json`: JSON file containing your liked songs data
- `liked_songs.txt`: Text file with a simple list of your liked songs

## Notes

- Downloads are organized by artist in the downloads directory
- The script uses the best audio quality available
- Metadata and thumbnails are embedded in the MP3 files

## Troubleshooting

- If you encounter authentication issues, delete the `.cache` file in the project directory and run the script again
- If downloads are failing, make sure you have the latest version of yt-dlp installed