import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pywhatkit as kit
import wikipedia

import VoiceEngine
import SpeechRecogniter

# Load environment variables
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

GPT_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-1B-distill"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "User-Agent": "Mozilla/5.0"
}


# -------------------- UTIL --------------------

def clean_query(command: str) -> str:
    return re.sub(r"(search|google|wikipedia|use wikipedia)", "", command, flags=re.IGNORECASE).strip()


def speak(text: str):
    VoiceEngine.say(text)


def listen() -> str:
    return str(SpeechRecogniter.getinput()).lower()


# -------------------- GOOGLE --------------------

def google(command: str):
    query = clean_query(command)
    speak(f"Searching {query} on Google")
    kit.search(query)


def query_search(command: str):
    query = clean_query(command)

    try:
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try featured snippets
        selectors = [
            ('Z0LcW t2b5Cf'),  # direct answer
            ('vk_gy vk_sh card-section sL6Rbf')  # knowledge panel
        ]

        for cls in selectors:
            result = soup.find(class_=cls)
            if result:
                speak(result.get_text())
                return

        # fallback
        google(query)

    except requests.RequestException:
        speak("Network error. Falling back to Google search.")
        google(query)


# -------------------- WIKIPEDIA --------------------

def wiki_search(command: str):
    query = clean_query(command)
    speak("Searching Wikipedia")

    try:
        results = wikipedia.search(query)

        if not results:
            raise ValueError("No results")

        summary = wikipedia.summary(results[0], sentences=2)
        speak(summary)

    except Exception:
        speak("I couldn't find it on Wikipedia. Want me to search on Google?")
        cmd = listen()

        if any(x in cmd for x in ["ok", "sure", "yes", "do"]):
            google(query)


# -------------------- HUGGINGFACE --------------------

def is_api_key_set() -> bool:
    return bool(HUGGINGFACE_API_TOKEN)


def show_api_key_help():
    url = "https://huggingface.co/docs/hub/security-tokens"
    speak("You need a Hugging Face API token to use this feature.")
    speak("Do you want me to open the guide?")

    cmd = listen()
    if any(x in cmd for x in ["ok", "sure", "yes", "open"]):
        google(url)


def gpt_chat(prompt: str):
    if not is_api_key_set():
        speak("Hugging Face API key is missing.")
        show_api_key_help()
        return

    payload = {"inputs": prompt}

    try:
        response = requests.post(
            GPT_MODEL_URL,
            headers=HEADERS,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        # safer parsing
        if isinstance(data, list) and "generated_text" in data[0]:
            text = data[0]["generated_text"]
            speak(text)
        else:
            speak("Sorry, I couldn't process that response.")

    except requests.RequestException:
        speak("Error contacting AI service.")
