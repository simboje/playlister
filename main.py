import json
import youtube_dl

def fetch_playlist_videos(playlist_url):
    ydl_opts = {
        'extract_flat': True,  # Get the video info without downloading
        'quiet': True,  # Suppress output
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

            # Check if 'entries' is in the returned dictionary
            if 'entries' in playlist_info:
                videos = [(entry['title'], entry['url']) for entry in playlist_info['entries']]
            else:
                print("No entries found in the playlist.")
                return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return videos

def save_to_json(playlist_name, videos):
    filename = f"{playlist_name}.json"
    with open(filename, 'w') as json_file:
        json.dump(videos, json_file, indent=4)

def main():
    playlist_url = input("Enter the YouTube playlist URL: ")
    playlist_name = input("Enter the name for the playlist file (without .json): ")

    videos = fetch_playlist_videos(playlist_url)
    if videos:  # Proceed only if videos are found
        save_to_json(playlist_name, videos)
        print(f"Playlist data saved to {playlist_name}.json")

if __name__ == "__main__":
    main()
