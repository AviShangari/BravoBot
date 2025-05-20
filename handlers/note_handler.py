def handle_take_note(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

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

    auto.take_note(note)
    speech.listen_for_keyboard_stop()
    speech.speak_and_log("Note saved.")


def handle_summarize_note(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    result = auto.summarize_last_note()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(result)


def handle_list_notes(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    result = auto.list_notes()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(result)
