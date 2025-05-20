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

from handlers.log_query_handler import handle_log_query
from handlers.llm_handler import handle_llm_query

from handlers.memory_handlers import (
    handle_remember,
    handle_recall,
    handle_forget
)

from handlers.note_handler import (
    handle_take_note,
    handle_summarize_note,
    handle_list_notes
)

from handlers.automation_handlers import (
    handle_open_youtube,
    handle_open_browser,
    handle_google_search,
    handle_search_youtube,
    handle_tell_time,
    handle_get_weather
)


logger = SessionLogger()
mem = MemoryStore()
speech = SpeechInterface()
llm = LLMInterface()
intent_model = IntentClassifier()
auto = Automation()

speech.logger = logger

context = {
    "logger": logger,
    "mem": mem,
    "speech": speech,
    "llm": llm,
    "auto": auto,
    "intent_model": intent_model
}

handlers = {
    "log_query": handle_log_query,
    "memory_remember": handle_remember,
    "memory_recall": handle_recall,
    "memory_forget": handle_forget,
    "take_note": handle_take_note,
    "summarize_note": handle_summarize_note,
    "list_notes": handle_list_notes,
    "open_youtube": handle_open_youtube,
    "open_browser": handle_open_browser,
    "google_search": handle_google_search,
    "search_youtube": handle_search_youtube,
    "tell_time": handle_tell_time,
    "get_weather": handle_get_weather,
    "llm_query": handle_llm_query,
    "llm_fallback": handle_llm_query,
}

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
    
        if command in handlers:
            handlers[command](user_input, context)
        else:
            speech.speak_and_log("Sorry, I don't know how to handle that yet.")

        print("---------------------------------------")

    except KeyboardInterrupt:
        print("Goodbye!")
        break
    except Exception as e:
        print("Error:", e)
        speech.speak_and_log("Sorry, something went wrong.")