import requests
from bs4 import BeautifulSoup
import json

def fetch_playlist_videos(playlist_url):
    # Fetch the HTML content of the playlist page
    response = requests.get(playlist_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the playlist: {response.status_code}")
        return []
    with open("response.html", "w", encoding='utf-8') as file:
        file.write(response.text)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all video links and titles
    videos = []
    nonvideos = []
    for a in soup.find_all('a', href=True):
        if '/watch?v=' in a['href']:
            title = a.get('title')
            link = 'https://www.youtube.com' + a['href']
            if title:  # Ensure the title is not None
                videos.append((title, link))
        else:
            title = a.get('title')
            link = 'https://www.youtube.com' + a['href']
            nonvideos.append((title, link))

    return videos, nonvideos

def save_to_json(playlist_name, videos):
    filename = f"{playlist_name}.json"
    with open(filename, 'w') as json_file:
        json.dump(videos, json_file, indent=4)

def main():
    playlist_url = input("Enter the YouTube playlist URL: ")
    playlist_name = input("Enter the name for the playlist file (without .json): ")

    videos, nonvideos = fetch_playlist_videos(playlist_url)
    if videos:
        save_to_json(playlist_name, videos)
        print(f"Playlist data saved to {playlist_name}.json")
    
    save_to_json(f"nonvideos.json", nonvideos)

if __name__ == "__main__":
    main()
