import os
import time
from playsound import playsound
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

# Dictionary of languages and their codes
lang_dict = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
    'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs',
    'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn',
    'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da',
    'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi',
    'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el',
    'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi',
    'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga',
    'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km',
    'korean': 'ko', 'kurdish': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv',
    'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms',
    'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'nepali': 'ne',
    'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt',
    'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'serbian': 'sr', 'sesotho': 'st',
    'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so',
    'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta',
    'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uzbek': 'uz',
    'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

# Capture voice and return recognized text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I did not understand that. Please try again.")
        return None
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results; {e}")
        return None

# Function to select the destination language
def destination_language():
    lang_input = lang_entry.get().lower()
    if lang_input in lang_dict:
        return lang_dict[lang_input]
    else:
        messagebox.showerror("Error", f"{lang_input} is not available. Please try another language.")
        return None

# Main function for translation and text-to-speech
def translate_and_speak():
    query = take_command()
    if query:
        to_lang = destination_language()
        if to_lang:
            translator = Translator()

            try:
                # Translate the input text to the selected destination language
                translated = translator.translate(query, dest=to_lang)
                translated_text = translated.text
                result_label.config(text=f"Translated Text: {translated_text}")

                # Convert translated text to speech and save it
                tts = gTTS(text=translated_text, lang=to_lang, slow=False)
                tts.save("captured_voice.mp3")

                # Play the audio file
                playsound('captured_voice.mp3')

                # Ensure file is closed before deletion
                time.sleep(1)

                # Remove the audio file after playing it
                os.remove('captured_voice.mp3')

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter UI setup
app = tk.Tk()
app.title("Voice Translator")
app.geometry("400x200")

lang_label = tk.Label(app, text="Enter the destination language (e.g., Hindi, Spanish):")
lang_label.pack(pady=10)

lang_entry = tk.Entry(app)
lang_entry.pack(pady=5)

translate_button = tk.Button(app, text="Translate and Speak", command=translate_and_speak)
translate_button.pack(pady=20)

result_label = tk.Label(app, text="")
result_label.pack(pady=5)

app.mainloop()
