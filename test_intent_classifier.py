import sys
import os
from intent_classifier import IntentClassifier

intent_model = IntentClassifier()

# === VECTOR MEMORY TESTS ===

def test_vector_remember_basic():
    result = intent_model.predict_intent("remember this for later")
    assert result == "vector_remember"

def test_vector_remember_natural():
    result = intent_model.predict_intent("store this in your memory")
    assert result == "vector_remember"

def test_vector_recall_basic():
    result = intent_model.predict_intent("what do you remember about me")
    assert result == "vector_recall"

def test_vector_recall_fuzzy():
    result = intent_model.predict_intent("can you recall anything I said?")
    assert result == "vector_recall"

# === AUTOMATION COMMANDS ===

def test_open_browser():
    result = intent_model.predict_intent("open the browser")
    assert result == "open_browser"

def test_open_youtube():
    result = intent_model.predict_intent("launch youtube")
    assert result == "open_youtube"

def test_tell_time():
    result = intent_model.predict_intent("what time is it?")
    assert result == "tell_time"

def test_get_weather():
    result = intent_model.predict_intent("what's the weather like?")
    assert result == "get_weather"

def test_search_youtube():
    result = intent_model.predict_intent("search youtube for relaxing music")
    assert result == "search_youtube"

def test_google_search():
    result = intent_model.predict_intent("search google for the capital of France")
    assert result == "google_search"

# === NOTES & MEMORY ===

def test_take_note():
    result = intent_model.predict_intent("take a note")
    assert result == "take_note"

def test_list_notes():
    result = intent_model.predict_intent("show me my notes")
    assert result == "list_notes"

def test_summarize_note():
    result = intent_model.predict_intent("summarize my last note")
    assert result == "summarize_note"

# === FALLBACK / SAFETY ===

def test_unknown_input_still_returns_string():
    result = intent_model.predict_intent("slkdfjskldfjskldjf")
    assert isinstance(result, str) and len(result) > 0
