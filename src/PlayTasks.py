import re
import webbrowser
import pywhatkit.misc as kit

import VoiceEngine
import SpeechRecogniter


def play(command: str):
    command = command.lower().strip()

    platform = detect_platform(command)
    query = clean_query(command)

    if not query:
        VoiceEngine.say("What do you want me to play?")
        return

    if platform == "youtube":
        play_youtube(query)
    elif platform == "spotify":
        play_spotify(query)
    else:
        ask_platform_and_retry(query)


def detect_platform(command: str) -> str | None:
    if "youtube" in command:
        return "youtube"
    if "spotify" in command:
        return "spotify"
    return None


def clean_query(command: str) -> str:
    # Remove trigger words and normalize spaces
    cleaned = re.sub(r"\b(play|on|youtube|spotify)\b", "", command)
    return re.sub(r"\s+", " ", cleaned).strip()


def ask_platform_and_retry(query: str):
    VoiceEngine.say("I can play on YouTube or Spotify. Which one do you prefer?")
    
    try:
        response = str(SpeechRecogniter.getinput()).lower()
    except Exception:
        VoiceEngine.say("I couldn't hear you clearly.")
        return

    if "youtube" in response:
        play_youtube(query)
    elif "spotify" in response:
        play_spotify(query)
    else:
        VoiceEngine.say("Sorry, I still couldn't determine the platform.")


def play_youtube(query: str):
    VoiceEngine.say(f"Playing {query} on YouTube")
    kit.playonyt(query)


def play_spotify(query: str):
    VoiceEngine.say(f"Playing {query} on Spotify")
    url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
    webbrowser.open_new_tab(url)
