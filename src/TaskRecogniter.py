import pywhatkit as kit
import PlayTasks as player
import GPTModel
import VoiceEngine
import SpeechRecogniter


WAKE_WORD = "hey computer"


# -------------------- UTIL --------------------

def speak(text: str):
    VoiceEngine.say(text)


def listen() -> str:
    return str(SpeechRecogniter.getinput()).lower()


def normalize(command: str) -> str:
    return command.lower().replace(WAKE_WORD, "").strip()


def has(command: str, *keywords) -> bool:
    return any(k in command for k in keywords)


# -------------------- HANDLERS --------------------

def handle_play(command: str):
    player.play(command)


def handle_open(command: str):
    GPTModel.google(command.replace("open", "").strip())


def handle_search(command: str):
    GPTModel.querysearch(command)


def handle_wikipedia(command: str):
    GPTModel.wiki_search(command)


def handle_screenshot(command: str):
    if has(command, "web screenshot"):
        query = command.replace("take", "").replace("web", "").replace("a", "").strip()
        kit.web_screenshot(query)
    else:
        kit.take_screenshot()


def handle_help():
    speak("I can open websites, play music, answer questions, and take screenshots.")
    speak("Say play followed by a song, or say open followed by a website.")
    speak("You can also ask me to search Google or Wikipedia.")


def handle_guide():
    speak("To unlock full features, you need a Hugging Face API token.")
    speak("Do you already have one?")

    cmd = listen()
    if has(cmd, "yes", "i have", "i got"):
        speak("Open your project folder, edit the .env file, and paste your API key.")
    else:
        speak("Do you want me to open the guide?")
        cmd = listen()
        if has(cmd, "yes", "sure", "open"):
            GPTModel.google("https://huggingface.co/docs/hub/security-tokens")


def handle_creator():
    speak("I was created by Vignesh as a fun project.")


def handle_about():
    speak("I am your personal AI assistant. I can help automate tasks and answer questions.")


def handle_gpt(command: str):
    GPTModel.gpt_chat(command)


# -------------------- MAIN ROUTER --------------------

def filter_command(command: str):
    print(command)

    if WAKE_WORD not in command.lower():
        return

    command = normalize(command)

    try:
        if has(command, "play"):
            return handle_play(command)

        if has(command, "open"):
            return handle_open(command)

        if has(command, "query search", "google search"):
            return handle_search(command)

        if has(command, "wikipedia"):
            return handle_wikipedia(command)

        if has(command, "screenshot"):
            return handle_screenshot(command)

        if has(command, "help", "what can you do"):
            return handle_help()

        if has(command, "guide me"):
            return handle_guide()

        if has(command, "user access token"):
            return handle_guide()

        if has(command, "who created you", "creator"):
            return handle_creator()

        if has(command, "about you"):
            return handle_about()

        # fallback to AI
        handle_gpt(command)

    except Exception as e:
        speak("Something went wrong.")
        print(f"Error: {e}")

    speak("Anything else?")
