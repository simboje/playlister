import os
import json
import yt_dlp
import sys

def download_audio(filename):
    # Derive the folder name from the filename (remove .json extension)
    download_folder = os.path.splitext(os.path.basename(filename))[0]
    
    # Load the JSON file
    with open(filename, 'r', encoding='utf-8') as f:
        video_list = json.load(f)
    
    # Create the folder for downloads if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Configure yt-dlp options for downloading audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        # Save the audio files in the derived folder with video title as the file name
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True  # Keep it quiet (no unnecessary output)
    }
    
    # Initialize yt-dlp and download each video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for entry in video_list:
            video_title = entry[0]
            video_url = entry[1]
            print(f"Downloading: {video_title} from {video_url}")
            try:
                # ydl.download([video_url])  # Download the video as audio
                print(f"Downloaded: {video_title}.mp3")
            except Exception as e:
                print(f"Failed to download {video_title}: {e}")

if __name__ == "__main__":
    # Check if filename is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.json>")
        sys.exit(1)
    
    # Run the download function
    download_audio(sys.argv[1])
