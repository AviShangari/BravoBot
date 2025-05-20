def handle_open_youtube(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    auto.open_youtube()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log("Opening YouTube")


def handle_open_browser(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    auto.open_browser()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log("Opening your browser")


def handle_google_search(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    auto.google_search(user_input)
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(f"Searching Google for {user_input}")


def handle_search_youtube(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    auto.search_youtube(user_input)
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(f"Searching YouTube for {user_input}")


def handle_tell_time(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    response = auto.tell_time()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(response)


def handle_get_weather(user_input, context):
    auto = context["auto"]
    speech = context["speech"]

    response = auto.get_weather()
    speech.listen_for_keyboard_stop()
    speech.speak_and_log(response)
