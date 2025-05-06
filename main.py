from speech import SpeechInterface
from llm import LLMInterface
from intent_classifier import IntentClassifier
from automation import Automation
import re

speech = SpeechInterface()
llm = LLMInterface()
intent_model = IntentClassifier()
auto = Automation()

while True:
    try:
        user_input = speech.listen()
        print(f'RECEIVED: {user_input}')

        # Interrupt check must be AFTER user_input is defined
        if any(word in user_input for word in ["wait", "hold on", "stop"]):
            speech.stop_speaking()
            continue

        # Only activate if 'ben' is a separate word
        if not re.search(r"\bben\b", user_input.lower()):
            print("Wake word 'ben' not found as separate word. Ignoring.")
            continue

        # Clean input for parsing
        user_input = user_input.lower().replace("ben", "").strip()
        command = intent_model.predict_intent(user_input)
        params = {"query": user_input}

        if command == "open_youtube":
            auto.open_youtube()
            speech.speak("Opening YouTube")

        elif command == "google_search":
            auto.google_search(user_input)
            speech.speak(f"Searching Google for {user_input}")

        elif command == "open_browser":
            auto.open_browser()
            speech.speak("Opening your browser")

        elif command == "tell_time":
            response = auto.tell_time()
            speech.speak(response)
        
        elif command == "search_youtube":
            auto.search_youtube(params["query"])
            speech.speak(f"Searching YouTube for {params['query']}")
        
        elif command == "get_weather":
            response = auto.get_weather()
            speech.speak(response)

        elif command in ["llm_query", "llm_fallback"]:
            use_openai = "use gpt" in user_input.lower()

            if use_openai:
                reply = llm.ask_with_openai(user_input)
            else:
                reply = llm.ask(user_input)  # default = Ollama

                if "sorry, i couldn't process that" in reply.lower():
                    print("Ollama failed, falling back to OpenAI...")
                    reply = llm.ask_with_openai(user_input)

            speech.speak(reply)

    except KeyboardInterrupt:
        print("Goodbye!")
        break
    except Exception as e:
        print("Error:", e)
        speech.speak("Sorry, something went wrong.")
