from speech import SpeechInterface
from llm import LLMInterface
from intent_classifier import IntentClassifier
from automation import Automation
import re
import time
from memory import MemoryStore
from utils import extract_memory_pair, format_memory_for_prompt
from session_log import SessionLogger
from time_utils import get_time_range_from_phrase

logger = SessionLogger()
mem = MemoryStore()
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
        
        logger.log("user", user_input)
        user_input = user_input.lower().replace("ben", "").strip()
        command = intent_model.predict_intent(user_input)
        params = {"query": user_input}

        if command == "memory_remember":
            speech.speak_and_log("What would you like me to remember?")
            value_input = speech.listen()
            key, value = extract_memory_pair(value_input)

            if key and value:
                mem.remember(key, value)
                speech.speak_and_log(f"I'll remember that your {key.replace('_', ' ')} is {value}.")
            else:
                speech.speak_and_log("Sorry, I couldn't understand what to remember.")


        elif command == "memory_recall":
            speech.speak_and_log("What would you like me to recall?")
            key_input = speech.listen()
            key = key_input.strip().lower().replace(" ", "_")
            value = mem.recall(key)
            if value:
                speech.speak_and_log(f"You told me your {key.replace('_', ' ')} is {value}.")
            else:
                speech.speak_and_log(f"I don't remember anything about your {key.replace('_', ' ')}.")

        elif command == "memory_forget":
            speech.speak_and_log("What memory should I forget?")
            key_input = speech.listen()
            key = key_input.strip().lower().replace(" ", "_")
            mem.forget(key)
            speech.speak_and_log(f"I’ve forgotten your {key.replace('_', ' ')}.")

        elif command == "open_youtube":
            auto.open_youtube()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log("Opening YouTube")

        elif command == "google_search":
            auto.google_search(user_input)
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(f"Searching Google for {user_input}")

        elif command == "open_browser":
            auto.open_browser()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log("Opening your browser")

        elif command == "tell_time":
            response = auto.tell_time()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(response)

        elif command == "search_youtube":
            auto.search_youtube(params["query"])
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(f"Searching YouTube for {params['query']}")

        elif command == "get_weather":
            response = auto.get_weather()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(response)
        
        elif command == "log_query":
            speech.speak_and_log("What time period are you referring to?")
            print("Bravobot: What time period are you referring to?")
            
            time_phrase = speech.listen()
            print(f"User Prompt: {time_phrase}")

            start, end = get_time_range_from_phrase(time_phrase)
            if not start or not end:
                speech.speak_and_log("Sorry, I couldn't understand that time frame.")
                print("Bravobot: Sorry, I couldn't understand that time frame.")
                continue

            logs = logger.get_logs_between(start, end)
            if not logs:
                speech.speak_and_log("I didn't find any conversations from that time.")
                print("Bravobot: I didn't find any conversation from that time.")
                print("---------------------------------------")
                continue

            # Step 1: Format as a conversation
            conversation = ""
            for ts, role, text in logs:
                role_name = "User" if role == "user" else "Bot"
                conversation += f"{role_name}: {text}\n"

            # Step 2: Summarize with LLM
            prompt = f"""Summarize the following conversation between a user and an assistant:

        {conversation}

        Respond with no more than 10 sentences summarizing what was said and discussed, in plain language."""
            
            summary = llm.ask(prompt)

            # Step 3: Speak + log the summary
            speech.speak_and_log("Here's a quick summary: " + summary)
            print(f"Bravobot: {summary}")


        elif command == "take_note":
            flag = False

            while not flag:
                speech.speak_and_log("What would you like to note?")
                print("BravoBot: What would you like to note?")
                note = speech.listen()
                print(f"User Prompt: {note}")
                speech.speak_and_log("Is this correct?")
                print("BravoBot: Is this correct? (Yes or no)")

                decision = speech.listen()
                if "yes" in decision.lower() or "yeah" in decision.lower():
                    flag = True
                else:
                    pass

            auto.take_note(note)
            speech.listen_for_keyboard_stop()
            speech.speak_and_log("Note saved.")

        elif command == "summarize_note":
            result = auto.summarize_last_note()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(result)

        elif command == "list_notes":
            result = auto.list_notes()
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(result)

        elif command in ["llm_query", "llm_fallback"]:
            use_openai = "use gpt" in user_input.lower()
            if use_openai:
                reply = llm.ask_with_openai(user_input)
            else:
                context = format_memory_for_prompt(mem)
                full_prompt = f"{context}\n\n{user_input}" if context else user_input
                reply = llm.ask(full_prompt)

                if "sorry, i couldn't process that" in reply.lower():
                    print("BravoBot: Ollama failed, falling back to OpenAI...")
                    reply = llm.ask_with_openai(user_input)
            speech.listen_for_keyboard_stop()
            speech.speak_and_log(reply)

        print("---------------------------------------")

    except KeyboardInterrupt:
        print("Goodbye!")
        break
    except Exception as e:
        print("Error:", e)
        speech.speak_and_log("Sorry, something went wrong.")