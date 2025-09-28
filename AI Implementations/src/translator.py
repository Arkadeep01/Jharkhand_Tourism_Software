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
    local_languages = ["santhali_trans.json", "mundari_trans.json"]

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
    recognizer = sr.Recognizer()

    # 🔑 Step 1: Wait for wake word "Hey Kyra"
    with sr.Microphone() as source:
        print("🎤 Say 'Hey Kyra' to activate...")
        while True:
            audio = recognizer.listen(source)
            try:
                trigger = recognizer.recognize_google(audio, language="en-IN").lower()
                if "hey kyra" in trigger:
                    speak("👋 Hi, I'm Kyra. I'm ready! Please speak now in " + src_lang)
                    break
            except sr.UnknownValueError:
                continue  # keep listening until "Hey Kyra"
            except sr.RequestError:
                return "⚠️ Could not connect to speech recognition service."

    # 🔑 Step 2: Capture user input after activation
    with sr.Microphone() as source:
        print("🎤 Listening for input...")
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
