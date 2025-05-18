from speech import SpeechInterface
from llm import LLMInterface
from intent_classifier import IntentClassifier
from automation import Automation
import re
import time

speech = SpeechInterface()
llm = LLMInterface()
intent_model = IntentClassifier()
auto = Automation()

while True:
    try:
        print("Waiting for input...")
        time.sleep(0.75)  # Allow mic to settle after any TTS
        user_input = speech.listen()

        if speech.skip_next_input:
            print("Skipping input after interruption.")
            speech.skip_next_input = False
            continue

        print(f'User prompt: {user_input}')

        if not re.search(r"\bben\b", user_input.lower()):
            print("Wake word 'Ben' not found. Ignoring.")
            print("---------------------------------------")
            continue

        user_input = user_input.lower().replace("ben", "").strip()
        command = intent_model.predict_intent(user_input)
        params = {"query": user_input}

        if command == "open_youtube":
            auto.open_youtube()
            speech.listen_for_keyboard_stop()
            speech.speak("Opening YouTube")

        elif command == "google_search":
            auto.google_search(user_input)
            speech.listen_for_keyboard_stop()
            speech.speak(f"Searching Google for {user_input}")

        elif command == "open_browser":
            auto.open_browser()
            speech.listen_for_keyboard_stop()
            speech.speak("Opening your browser")

        elif command == "tell_time":
            response = auto.tell_time()
            speech.listen_for_keyboard_stop()
            speech.speak(response)

        elif command == "search_youtube":
            auto.search_youtube(params["query"])
            speech.listen_for_keyboard_stop()
            speech.speak(f"Searching YouTube for {params['query']}")

        elif command == "get_weather":
            response = auto.get_weather()
            speech.listen_for_keyboard_stop()
            speech.speak(response)
        
        elif command == "take_note":
            auto.take_note(user_input)
            speech.listen_for_keyboard_stop()
            speech.speak("Note saved.")

        elif command == "summarize_note":
            result = auto.summarize_last_note()
            speech.listen_for_keyboard_stop()
            speech.speak(result)

        elif command == "list_notes":
            result = auto.list_notes()
            speech.listen_for_keyboard_stop()
            speech.speak(result)

        elif command in ["llm_query", "llm_fallback"]:
            use_openai = "use gpt" in user_input.lower()
            if use_openai:
                reply = llm.ask_with_openai(user_input)
            else:
                reply = llm.ask(user_input)
                if "sorry, i couldn't process that" in reply.lower():
                    print("Ollama failed, falling back to OpenAI...")
                    reply = llm.ask_with_openai(user_input)
            speech.listen_for_keyboard_stop()
            speech.speak(reply)

        print("---------------------------------------")

    except KeyboardInterrupt:
        print("Goodbye!")
        break
    except Exception as e:
        print("Error:", e)
        speech.speak("Sorry, something went wrong.")