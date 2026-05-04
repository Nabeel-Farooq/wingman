import sys
import speech_recognition as sr
import VoiceEngine


listener = sr.Recognizer()


def speak(text: str):
    VoiceEngine.say(text)


def get_input(timeout: int = 5, phrase_time_limit: int = 10) -> str:
    """Listen and return recognized speech as lowercase string"""

    with sr.Microphone() as source:
        print("🎤 Listening...")
        
        # Adjust for ambient noise (important!)
        listener.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = listener.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

            command = listener.recognize_google(audio).lower().strip()
            print(f"🗣️ You said: {command}")

            # Optional: echo back
            speak(command)

            # Exit commands
            if command in {"exit", "kill", "end process"}:
                speak("Shutting down")
                sys.exit()

            if command == "stop":
                return ""

            return command

        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out")
            return ""

        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""

        except sr.RequestError:
            print("🌐 API unavailable")
            speak("Speech service is unavailable")
            return ""

        except Exception as e:
            print(f"⚠️ Error: {e}")
            return ""
