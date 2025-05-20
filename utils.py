import re

def extract_memory_pair(text):
    """
    Extracts a (key, value) pair from a sentence like:
    'remember that my favorite food is pizza'
    Returns ('favorite_food', 'pizza')
    """
    match = re.search(r"my (.+?) is (.+)", text)
    if match:
        key = match.group(1).strip().lower().replace(" ", "_")
        value = match.group(2).strip()
        return key, value
    return None, None


def format_memory_for_prompt(mem):
    """
    Returns a string like:
    'User previously said: favorite_food = pizza, diet = vegetarian.'
    """
    memory_items = mem.list_all()
    if not memory_items:
        return ""
    facts = [f"{k.replace('_', ' ')} is {v}" for k, v in memory_items]
    return "User previously said: " + ", ".join(facts) + "."
