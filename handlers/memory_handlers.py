from utils import extract_memory_pair

def handle_remember(user_input, context):
    mem = context["mem"]
    speech = context["speech"]

    speech.speak_and_log("What would you like me to remember?")
    value_input = speech.listen()
    key, value = extract_memory_pair(value_input)

    if key and value:
        mem.remember(key, value)
        speech.speak_and_log(f"I'll remember that your {key.replace('_', ' ')} is {value}.")
    else:
        speech.speak_and_log("Sorry, I couldn't understand what to remember.")


def handle_recall(user_input, context):
    mem = context["mem"]
    speech = context["speech"]

    speech.speak_and_log("What would you like me to recall?")
    key_input = speech.listen()
    key = key_input.strip().lower().replace(" ", "_")
    value = mem.recall(key)

    if value:
        speech.speak_and_log(f"You told me your {key.replace('_', ' ')} is {value}.")
    else:
        speech.speak_and_log(f"I don't remember anything about your {key.replace('_', ' ')}.")


def handle_forget(user_input, context):
    mem = context["mem"]
    speech = context["speech"]

    speech.speak_and_log("What memory should I forget?")
    key_input = speech.listen()
    key = key_input.strip().lower().replace(" ", "_")
    mem.forget(key)
    speech.speak_and_log(f"I’ve forgotten your {key.replace('_', ' ')}.")
