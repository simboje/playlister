import os
import json
import yt_dlp
import sys
import shutil
import pyminizip

def download_audio(filename):
    # Derive the folder name from the filename (remove .json extension)
    download_folder = 'download_dir'
    playlist_name = os.path.splitext(os.path.basename(filename))[0]
    
    # Load the JSON file with utf-8 encoding to avoid UnicodeDecodeError
    with open(filename, 'r', encoding='utf-8') as f:
        video_list = json.load(f)
    
    if os.path.exists(download_folder):
        shutil.rmtree(download_folder)

    os.makedirs(download_folder)
    
    # Configure yt-dlp options for downloading audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Set to 320 kbps for highest quality MP3
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
            try:
                ydl.download([video_url])  # Download the video as audio
                print(f"Downloaded: {video_title}.mp3")
            except Exception as e:
                print(f"Failed to download {video_title}: {e}")

    # Zip the entire folder using shutil
    zip_output = playlist_name + ".zip"
    
    try:
        # Use shutil.make_archive to zip the whole folder
        shutil.make_archive(download_folder, 'zip', download_folder)
        print(f"Folder '{download_folder}' has been zipped successfully.")
    except Exception as e:
        print(f"Error while zipping the folder: {e}")
        return
    
    unprotected = f"{download_folder}.zip"
    # Add password protection to the zip file
    password = "passwordfiles246"
    try:
        pyminizip.compress(unprotected, None, unprotected.replace('.zip', '_protected.zip'), password, 1)
        print(f"Zipped file '{unprotected}' is now protected and saved as '{unprotected.replace('.zip', '_protected.zip')}'.")
        
        # Optionally, remove the original unprotected zip file if needed
        os.remove(unprotected)
    except Exception as e:
        print(f"Error while adding password to zip: {e}")

if __name__ == "__main__":
    # Check if filename is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.json>")
        sys.exit(1)
    
    # Run the download function
    download_audio(sys.argv[1])
