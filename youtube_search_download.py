import os
import yt_dlp
from youtubesearchpython import VideosSearch

def create_download_folder():
    folder_name = 'direct youtube Rips'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def search_youtube(query):
    search = VideosSearch(query, limit=2)
    results = search.result()['result']
    return results

def display_results(results):
    print('\nSearch Results:')
    for i, video in enumerate(results, 1):
        print(f"\n{i}. {video['title']}")
        print(f"   Duration: {video['duration']}")
        print(f"   Channel: {video['channel']['name']}")
        print(f"   Views: {video['viewCount']['short']}")

def download_video(video_url, folder_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(folder_name, '%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            return True
        except Exception as e:
            print(f"Error downloading: {e}")
            return False

def main():
    query = input("Enter your search query: ")
    results = search_youtube(query)
    
    if not results:
        print("No results found.")
        return
    
    display_results(results)
    
    choice = input("\nEnter 1 or 2 to download your preferred result (or any other key to cancel): ")
    
    if choice in ['1', '2']:
        selected_index = int(choice) - 1
        if selected_index < len(results):
            folder_name = create_download_folder()
            video_url = results[selected_index]['link']
            print(f"\nDownloading: {results[selected_index]['title']}")
            if download_video(video_url, folder_name):
                print("\nDownload completed successfully!")
            else:
                print("\nDownload failed.")
        else:
            print("Invalid selection.")
    else:
        print("Download cancelled.")

if __name__ == '__main__':
    main()