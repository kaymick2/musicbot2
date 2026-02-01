#!/usr/bin/env python3
import os
import argparse
import os
import argparse
from download_songs import download_songs
from download_songs import download_songs

def main():
    parser = argparse.ArgumentParser(description="Download your Spotify music from YouTube")
    parser.add_argument("-d", "--download-only", action="store_true", 
                        help="Skip Spotify API and only download songs from existing JSON")
    parser.add_argument("-o", "--output-dir", default="downloads",
                        help="Directory to save downloaded songs (default: downloads)")
    parser.add_argument("-f", "--file", default="liked_songs.json",
                        help="JSON file containing songs to download (default: liked_songs.json)")
    args = parser.parse_args()
    
    if not args.download_only:
        from spotify_interface import main_menu
        main_menu()
    
    json_file = args.file
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found. Run without --download-only first.")
        return
    
    print("\nDownloading songs from YouTube...")
    download_songs(json_file=json_file, output_dir=args.output_dir)
    
    print("\nProcess complete! Your music has been downloaded.")
    print("Note: Songs are saved with correct metadata from Spotify.")

if __name__ == "__main__":
    main()