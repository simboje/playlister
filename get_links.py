import requests
import re
import json
import argparse

def fetch_playlist_videos(playlist_url):
    # Fetch the HTML content of the playlist page
    response = requests.get(playlist_url)

    # Write the entire response to a file for debugging
    with open("response.html", "w", encoding='utf-8') as file:
        file.write(response.text)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the playlist: {response.status_code}")
        return []

    # Extract titles and URLs using regex
    videos = []
    pattern = r'"title":\{"runs":\[\{"text":"(.*?)"\}\],"accessibility":.*?"navigationEndpoint":.*?"url":"(/watch\?v=.*?)\\u0026.*?}'
    matches = re.findall(pattern, response.text)

    for title, url in matches:
        full_url = f'https://www.youtube.com{url.replace("\\u0026", "&")}'
        videos.append((title, full_url))

    return videos

def save_to_json(playlist_name, videos):
    filename = f"{playlist_name}.json"
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(videos, json_file, indent=4,ensure_ascii=False)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch YouTube playlist videos.")
    parser.add_argument("playlist_url", help="The URL of the YouTube playlist.")
    parser.add_argument("playlist_name", help="The name for the playlist file (without .json).")
    
    args = parser.parse_args()

    videos = fetch_playlist_videos(args.playlist_url)
    if videos:
        save_to_json(args.playlist_name, videos)
        print(f"Playlist data saved to {args.playlist_name}.json")

if __name__ == "__main__":
    main()
