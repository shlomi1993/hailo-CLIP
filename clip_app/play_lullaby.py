# When called will activate a lullaby / song / melody


# sudo apt update 
# sudo apt install mpg321 for cli
# mpg321 /home/hailo/Downloads/brahmsx27-lullaby-160672.mp3 for cli
# mpg321 brahms-lullaby.mp3 for cli playing mp3
# Add to install.sh
# curl -L "https://drive.usercontent.google.com/uc?id=1Myk5VzIQWYDbjp-zYiFjUwQn15HQyuPU&export=download" -o brahms-lullaby.mp3 
from playsound import playsound
import os

REPO_ROOT_DIRECTORY = "/home/hailo/hackathon24/hailo-CLIP" #TODO: mark as define in a util directory?
DEFAULT_MP3_FILE = os.path.join(REPO_ROOT_DIRECTORY, "resources", "brahms-lullaby.mp3")
def play_mp3(mp3_file_path=DEFAULT_MP3_FILE):
    try:
        # Play the MP3 file
        print("Playing the MP3 file...")
        playsound(mp3_file_path)
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")

# if __name__ == "__main__":
#     play_mp3()
