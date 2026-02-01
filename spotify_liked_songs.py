import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def get_liked_songs():
    # Set up authentication with Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="be0c8322777849e5ad99363fc81ce39a",
        client_secret="a7cb558afe3f4b238475108fa71186bc",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-library-read"
    ))

    # Get user's saved tracks (liked songs)
    results = sp.current_user_saved_tracks(limit=50)
    songs = []
    tracks_data = []

    # Handle pagination to get all liked songs
    while results:
        for item in results['items']:
            track = item['track']
            title = track['name']
            artist = track['artists'][0]['name']
            songs.append(f"{title} - {artist}")
            
            # Store detailed track information
            track_info = {
                'title': title,
                'artist': artist,
                'album': track['album']['name'],
                'spotify_url': track['external_urls']['spotify'],
                'duration_ms': track['duration_ms'],
                'search_query': f"{title} {artist}"
            }
            tracks_data.append(track_info)
        
        # Get next page of results if available
        if results['next']:
            results = sp.next(results)
        else:
            break

    # Save list as text file (for simple viewing)
    with open("liked_songs.txt", "w", encoding="utf-8") as f:
        for song in songs:
            f.write(song + "\n")
    
    # Save detailed information as JSON
    with open("liked_songs.json", "w", encoding="utf-8") as f:
        json.dump(tracks_data, f, indent=4)
    
    print(f"Successfully retrieved {len(songs)} liked songs.")
    print("Saved to liked_songs.txt and liked_songs.json")
    
    return tracks_data

if __name__ == "__main__":
    get_liked_songs()
