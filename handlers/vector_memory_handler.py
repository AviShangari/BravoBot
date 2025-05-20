def handle_vector_remember(user_input, context):
    speech = context["speech"]
    vector_mem = context["vector_mem"]

    speech.speak_and_log("What would you like me to remember?")
    fact = speech.listen()
    vector_mem.add(fact)
    speech.speak_and_log("Got it. I've stored that in memory.")


def handle_vector_recall(user_input, context):
    speech = context["speech"]
    vector_mem = context["vector_mem"]
    llm = context["llm"]

    top_matches = vector_mem.query(user_input, top_k=3)
    if not top_matches:
        speech.speak_and_log("I couldn't find anything relevant in memory.")
        return

    # Inject vector memory into prompt
    memory_context = "\n".join(f"User previously said: {fact}" for fact in top_matches)
    final_prompt = f"{memory_context}\n\n{user_input}"
    response = llm.ask(final_prompt)

    speech.listen_for_keyboard_stop()
    speech.speak_and_log(response)
