import speech_recognition as sr

def speech_to_text(filename: str) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio).lower()
            return recognized_text
    except sr.RequestError as e:
        print(f"API Error: Could not request results - {e}")
        return None
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return None
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return None