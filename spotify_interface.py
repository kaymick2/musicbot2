import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
import os
from dotenv import load_dotenv
import sys

console = Console()
# Load environment variables from .env file
load_dotenv()

# Access environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

def setup_spotify():
    """Initialize and return authenticated Spotify client"""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-library-read playlist-read-private"
    ))

def get_user_playlists(sp: spotipy.Spotify) -> List[Dict]:
    """Fetch all playlists for the current user"""
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        for item in results['items']:
            playlists.append({
                'name': item['name'],
                'id': item['id'],
                'tracks_total': item['tracks']['total'],
                'owner': item['owner']['display_name']
            })
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return playlists

def get_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> List[Dict]:
    """Get all tracks from a specific playlist"""
    tracks_data = []
    results = sp.playlist_tracks(playlist_id)
    
    while results:
        for item in results['items']:
            if not item['track']:
                continue
            
            track = item['track']
            track_info = {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'spotify_url': track['external_urls']['spotify'],
                'duration_ms': track['duration_ms'],
                'search_query': f"{track['name']} {track['artists'][0]['name']}"
            }
            tracks_data.append(track_info)
        
        if results['next']:
            results = sp.next(results)
        else:
            break
    
    return tracks_data

def display_playlists(playlists: List[Dict]):
    """Display playlists in a formatted table"""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim")
    table.add_column("Name")
    table.add_column("Tracks")
    table.add_column("Owner")
    
    for idx, playlist in enumerate(playlists, 1):
        table.add_row(
            str(idx),
            playlist['name'],
            str(playlist['tracks_total']),
            playlist['owner']
        )
    
    console.print(table)

def save_tracks_to_files(tracks: List[Dict], filename_prefix: str = ""):
    """Save tracks data to both JSON and TXT files"""
    # Save detailed information as JSON
    json_filename = f"{filename_prefix}songs.json" if filename_prefix else "liked_songs.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(tracks, f, indent=4)
    
    # Save simple list as text file
    txt_filename = f"{filename_prefix}songs.txt" if filename_prefix else "liked_songs.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        for track in tracks:
            f.write(f"{track['title']} - {track['artist']}\n")
    
    return json_filename, txt_filename

def list_playlists():
    """List all available playlists for the current user"""
    sp = setup_spotify()
    playlists = get_user_playlists(sp)
    display_playlists(playlists)
    return playlists

def main_menu():
    """Display main menu and handle user input"""
    sp = setup_spotify()
    
    while True:
        console.print("\n[bold cyan]Spotify Music Downloader[/bold cyan]")
        console.print("1. Download Liked Songs")
        console.print("2. Download from Playlist")
        console.print("3. Exit")
        
        choice = IntPrompt.ask("\nEnter your choice", choices=["1", "2", "3"])
        
        if choice == 1:
            console.print("\n[bold]Fetching your liked songs...[/bold]")
            results = sp.current_user_saved_tracks(limit=50)
            tracks = []
            
            with console.status("[bold green]Loading liked songs...") as status:
                while results:
                    for item in results['items']:
                        track = item['track']
                        track_info = {
                            'title': track['name'],
                            'artist': track['artists'][0]['name'],
                            'album': track['album']['name'],
                            'spotify_url': track['external_urls']['spotify'],
                            'duration_ms': track['duration_ms'],
                            'search_query': f"{track['name']} {track['artists'][0]['name']}"
                        }
                        tracks.append(track_info)
                    
                    if results['next']:
                        results = sp.next(results)
                    else:
                        break
            
            json_file, txt_file = save_tracks_to_files(tracks)
            console.print(f"\n[green]Successfully saved {len(tracks)} liked songs to {json_file} and {txt_file}[/green]")
            
        elif choice == 2:
            console.print("\n[bold]Fetching your playlists...[/bold]")
            playlists = get_user_playlists(sp)
            display_playlists(playlists)
            
            playlist_choice = IntPrompt.ask(
                "\nEnter playlist number to download (0 to cancel)",
                choices=[str(i) for i in range(len(playlists) + 1)]
            )
            
            if playlist_choice == 0:
                continue
            
            selected_playlist = playlists[playlist_choice - 1]
            console.print(f"\n[bold]Fetching tracks from '{selected_playlist['name']}'...[/bold]")
            
            tracks = get_playlist_tracks(sp, selected_playlist['id'])
            json_file, txt_file = save_tracks_to_files(tracks, f"playlist_{selected_playlist['id']}_")
            
            console.print(f"\n[green]Successfully saved {len(tracks)} tracks to {json_file} and {txt_file}[/green]")
            
        else:
            break

if __name__ == "__main__":
    main_menu()
