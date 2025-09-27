from db import translations_col
import openai
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak out the text"""
    engine.say(text)
    engine.runAndWait()

def translator(text, src_lang, tgt_lang):
    """
    Translate text:
    - English/Hindi → GPT
    - Santhali/Mundari (local languages) → MongoDB datasets
    """
    local_languages = ["Santhali", "Mundari"]

    # Use GPT for English/Hindi translations
    if src_lang in ["English", "Hindi"] or tgt_lang in ["English", "Hindi"]:
        prompt = f"Translate this text from {src_lang} to {tgt_lang}: {text}"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        translated = response["choices"][0]["text"].strip()

    # Use MongoDB dataset for local languages
    elif src_lang in local_languages or tgt_lang in local_languages:
        entry = translations_col.find_one({
            "source_text": text,
            "source_lang": src_lang,
            "target_lang": tgt_lang
        })
        translated = entry["translated_text"] if entry else "Translation not available."

    else:
        translated = "Translation not available for this language pair."

    # Speak the translation
    speak(translated)
    return translated

def listen_and_translate(src_lang, tgt_lang, recog_lang_code="en-IN"):
    """
    Listen via microphone and translate.
    recog_lang_code: Google Speech Recognition code (e.g., "en-IN" for English)
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech
        speech_text = recognizer.recognize_google(audio, language=recog_lang_code)
        print(f"You said ({src_lang}): {speech_text}")

        # Translate
        translated = translator(speech_text, src_lang, tgt_lang)
        print(f"Translated ({tgt_lang}): {translated}")
        return translated

    except sr.UnknownValueError:
        return "⚠️ Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"⚠️ Could not request results; {e}"

# Example usage
if __name__ == "__main__":
    # English → Santhali example
    listen_and_translate("English", "Santhali", recog_lang_code="en-IN")
