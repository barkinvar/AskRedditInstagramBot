from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track
import subprocess

def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    print_step("Saving Text to MP3 files...")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    subprocess.run(['edge-tts', "--voice", "tr-TR-EmelNeural", '--text', str(reddit_obj["thread_title"]), '--write-media', "assets/mp3/title.mp3"])
    length += MP3(f"assets/mp3/title.mp3").info.length

    try:
        Path(f"assets/mp3/posttext.mp3").unlink()
    except OSError as e:
        pass

    if reddit_obj["thread_post"] != "":
        subprocess.run(['edge-tts', "--voice", "tr-TR-EmelNeural", '--text', str(reddit_obj["thread_post"]), '--write-media', "assets/mp3/posttext.mp3"])
        length += MP3(f"assets/mp3/posttext.mp3").info.length

    for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 50 seconds. This can be longer, but this is just a good starting point
        if length > 50:
            break
        subprocess.run(['edge-tts', "--voice", "tr-TR-EmelNeural", '--text', str(comment["comment_body"]), '--write-media', f"assets/mp3/{idx}.mp3"])
        length += MP3(f"assets/mp3/{idx}.mp3").info.length

    print_substep("Saved Text to MP3 files successfully.", style="bold green")
    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
