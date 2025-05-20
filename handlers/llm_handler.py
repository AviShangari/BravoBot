def handle_llm_query(user_input, context):
    llm = context["llm"]
    mem = context["mem"]
    speech = context["speech"]

    use_openai = "use gpt" in user_input.lower()
    if use_openai:
        reply = llm.ask_with_openai(user_input)
    else:
        memory_context = context_string(mem)
        prompt = f"{memory_context}\n\n{user_input}" if memory_context else user_input
        reply = llm.ask(prompt)

        if "sorry, i couldn't process that" in reply.lower():
            print("BravoBot: Ollama failed, falling back to OpenAI...")
            reply = llm.ask_with_openai(user_input)

    speech.listen_for_keyboard_stop()
    speech.speak_and_log(reply)


def context_string(mem):
    """Helper function to format memory for the prompt."""
    memory_items = mem.list_all()
    if not memory_items:
        return ""
    facts = [f"{k.replace('_', ' ')} is {v}" for k, v in memory_items]
    return "User previously said: " + ", ".join(facts) + "."
