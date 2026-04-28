import json
import subprocess
import os
import time
import threading
import sys
import select
import queue
import glob
from concurrent.futures import ThreadPoolExecutor

def get_video_title(query):
    """Get the title of the first YouTube search result without downloading"""
    try:
        # Add 'Audio' to the search query and use the first result
        audio_query = f"{query} Audio"
        result = subprocess.run([
            "yt-dlp",
            "--js", "node",
            f"ytsearch1:{audio_query}",
            "--get-title",
            "--skip-download"
        ], capture_output=True, text=True)
        
        # Get the first line of output (the title)
        title = result.stdout.strip().split('\n')[0]
        return title
    except Exception as e:
        return f"Could not retrieve title: {e}"

def wait_for_bypass(seconds=3):
    """Wait for user input to bypass download"""
    print(f"Press 'b' within {seconds} seconds to skip this download...")
    
    # Check if input is available within the time limit
    i, o, e = select.select([sys.stdin], [], [], seconds)
    
    if i:
        key = sys.stdin.readline().strip().lower()
        return key == 'b'
    return False

def download_single_song(song, i, total_songs, output_dir):
    """Download a single song with title preview and bypass option"""
    query = song['search_query']
    
    print(f"\n[{i}/{total_songs}] Processing: {song['title']} - {song['artist']}")
    
    try:
        # Get video title first
        video_title = get_video_title(query)
        print(f"Found YouTube video: {video_title}")
        
        # Give user option to bypass
        if wait_for_bypass():
            print(f"Skipping download for: {song['title']}")
            return
        
        print(f"Downloading: {video_title}")
        
        # Add 'Audio' to the search query and use the first result
        audio_query = f"{query} Audio"
        # Use yt-dlp to download the audio
        subprocess.run([
            "yt-dlp",
            "--js", "node",
            f"ytsearch1:{audio_query}",
            "--format", "bestaudio[ext!=mhtml]/bestaudio/best[ext!=mhtml]",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Best quality
            "--embed-thumbnail",
            "--add-metadata",
            "--parse-metadata", f"title:{song['title']}",
            "--parse-metadata", f"artist:{song['artist']}",
            "--parse-metadata", f"album:{song['album']}",
            "--output", f"{output_dir}/%(title)s - %(artist)s.%(ext)s",
            "--no-playlist"  # Prevent downloading multiple versions of the same song
        ])
        cleanup_patterns = ("*.mhtml", "*.webp", "*.jpg")
        for pattern in cleanup_patterns:
            for leftover_file in glob.glob(os.path.join(output_dir, pattern)):
                try:
                    os.remove(leftover_file)
                except OSError:
                    pass
        
    except Exception as e:
        print(f"Error processing {song['title']}: {e}")

def select_json_file():
    """Display available JSON files and let user select one"""
    # Get list of JSON files in current directory
    json_files = [f for f in os.listdir() if f.endswith('.json')]
    
    if not json_files:
        print("No JSON files found in the current directory.")
        return None
    
    print("\nAvailable playlist files:")
    for i, file in enumerate(json_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = input("\nEnter the number of the file to download from (or 'q' to quit): ")
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(json_files):
                return json_files[index]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def download_songs(json_file="liked_songs.json", output_dir="downloads", max_workers=3):
    """Download songs with title preview, bypass option, and parallel downloads"""
    # Let user select JSON file if none specified
    if json_file == "liked_songs.json":
        selected_file = select_json_file()
        if selected_file is None:
            print("Download cancelled.")
            return
        json_file = selected_file
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the songs data from JSON file
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            songs = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found. Run spotify_liked_songs.py first.")
        return
    
    total_songs = len(songs)
    print(f"Found {total_songs} songs to download")
    print(f"Using up to {max_workers} parallel downloads")
    print("For each song, you'll see the YouTube video title and have 3 seconds to press 'b' to skip it")
    
    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        futures = []
        for i, song in enumerate(songs, 1):
            future = executor.submit(download_single_song, song, i, total_songs, output_dir)
            futures.append(future)
            # Small delay between submissions to avoid overwhelming the terminal output
            time.sleep(0.5)
        
        # Wait for all downloads to complete
        for future in futures:
            future.result()
    
    print("\nDownload complete!")

if __name__ == "__main__":
    download_songs()
