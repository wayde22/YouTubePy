from pytube import YouTube
import os
from pathlib import Path
from timeit import default_timer as timer
import time

source = 'D:/Dev/Python_Projects/YouTubePy'
destination = 'D:/Video Capture/Youtube Videos'
global start_timer;
global end_timer;

# Colors for the terminal
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def clear_bash_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_youtube_object(link):
    youtubeObject = YouTube(link)
    print(f"\nGetting {BOLD}{WARNING}\"{youtubeObject.title}\"{ENDC} video......")
    highResVideo = youtubeObject.streams.get_highest_resolution()
    return highResVideo


def download(obj):
    try:
        print(f"Attempting to download {BOLD}{OKBLUE}\"{obj.title}\"{ENDC}.....\n")
        obj.download()
        # Check if the file exists after download
        source_file = Path(source)/f'{obj.title}.mp4'
        print(f"File: {source_file}")
        print(f"Exist: {source_file.exists()}")
        # count = 0
        # ## should try to make this async
        # while not source_file.exists():
        #     count = count + 1
        #     print(f"Exist {count}: {source_file.exists()}")
        #     time.sleep(1)  # Pause for 1 second before checking again

        move_files(obj.title)

        end_timer = timer()
        print(f"{BOLD}{OKGREEN}\"{obj.title}\"{ENDC} download has completed successfully in %.4f seconds !" % (end_timer - start_timer) )
    except Exception as e:
        print(f"An error has occurred: {e}")


# def move_files(obj_title):
    # source_file = Path(source)/f'{obj_title}.mp4'
    # destination_file = Path(destination)/f'{obj_title}.mp4'
    # source_file.rename(destination_file)

def move_files(obj_title):
    source_file = Path(source)/f'{obj_title}.mp4'
    destination_file = Path(destination)/f'{obj_title}.mp4'

    time.sleep(3)

    print(f"Source file: {source_file}")
    print(f"Destination file: {destination_file}")

    if source_file.exists():
        source_file.rename(destination_file)
        print("File moved successfully!")
    else:
        print("Source file does not exist!")


if __name__ == "__main__":
    clear_bash_terminal()
    youtubeLink = input("Enter the YouTube video URL: ")
    start_timer = timer()
    youtubeVideo = get_youtube_object(youtubeLink)
    download(youtubeVideo)
