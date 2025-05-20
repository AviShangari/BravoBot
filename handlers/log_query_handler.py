from time_utils import get_time_range_from_phrase

def handle_log_query(user_input, context):
    logger = context["logger"]
    llm = context["llm"]
    speech = context["speech"]

    speech.speak_and_log("What time period are you referring to?")
    print("Bravobot: What time period are you referring to?")

    time_phrase = speech.listen()
    print(f"User Prompt: {time_phrase}")

    start, end = get_time_range_from_phrase(time_phrase)
    if not start or not end:
        speech.speak_and_log("Sorry, I couldn't understand that time frame.")
        print("Bravobot: Sorry, I couldn't understand that time frame.")
        return

    logs = logger.get_logs_between(start, end)
    if not logs:
        speech.speak_and_log("I didn't find any conversations from that time.")
        print("Bravobot: I didn't find any conversation from that time.")
        print("---------------------------------------")
        return

    conversation = ""
    for ts, role, text in logs:
        role_name = "User" if role == "user" else "Bot"
        conversation += f"{role_name}: {text}\n"

    prompt = f"""Summarize the following conversation between a user and an assistant:

{conversation}

Respond with no more than 10 sentences summarizing what was said and discussed, in plain language."""
    
    summary = llm.ask(prompt)
    speech.speak_and_log("Here's a quick summary: " + summary)
    print(f"Bravobot: {summary}")
