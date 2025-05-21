# BravoBot

**BravoBot** is an offline-first, voice-powered AI assistant that combines natural language understanding, persistent memory, and modular architecture. Built for speed, usability, and extensibility, it's your own LLM-powered assistant — no internet required.

---

## 🚀 Features

- **Voice Commands** – Talk to BravoBot using your microphone
- **Vector Memory** – Remembers full sentences semantically (e.g., "I love hiking in the rain")
- **Modular Handlers** – Each intent is routed through a clean, plugin-style handler system
- **Session Logging** – Automatically logs all conversations with timestamps
- **Offline-First Design** – Runs with local LLMs and sentence transformers
- **Optional Online Fallback** – Uses OpenAI if Ollama fails
- **CLI & Keyboard Control** – Stop speech with `Shift+Q`; debug/test via CLI

---

## 🛠️ Tech Stack

- Python 3.11+
- `whisper`, `pyttsx3` – Voice input/output
- `sentence-transformers`, `faiss` – Vector memory
- `Ollama`, `OpenAI` – LLMs
- `sqlite3`, `pickle` – Memory and logs
- `pytest` – Unit testing

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/BravoBot.git
cd BravoBot
pip install -r requirements.txt
```

Also install:

```bash
# For audio input/output
brew install ffmpeg         # macOS
choco install ffmpeg        # Windows
sudo apt install ffmpeg     # Linux

# For running local LLMs
ollama run llama3
```

---

## ▶️ Running BravoBot

To start the assistant:

```bash
python main.py
```

Optional CLI flags (coming soon):

```bash
--list-memory                 # View all stored vector memories
--clear-logs                  # Delete all session logs
--debug-intent "your text"   # See which intent would be triggered
```

Example:

```bash
python main.py --debug-intent "what time is it?"
```

---

## 🗣️ Example Voice Commands

| You Say                          | BravoBot Does                        |
| -------------------------------- | ------------------------------------ |
| What time is it?                 | Tells the current time               |
| Remember that I love hiking      | Stores the sentence in vector memory |
| What do I like to do?            | Recalls memory and answers via LLM   |
| Open YouTube                     | Launches YouTube                     |
| Search Google for Python testing | Opens a Google search                |

---

## 🧠 Architecture

```
+-------------+      +--------------------+      +---------------------+
|   You Talk  | -->  |  Intent Classifier | -->  |   Plugin Handler     |
+-------------+      +--------------------+      +---------------------+
                                                  |
                                                  v
                          +-------------------------------------------+
                          |   Vector Memory / LLM / Logger / Notes    |
                          +-------------------------------------------+
```

---

## ✅ Unit Testing

BravoBot includes unit tests for:

- Vector memory (`vector_store.py`)
- Intent classification (`intent_classifier.py`)
- Session logging (`session_log.py`)

To run tests:

```bash
pytest
```

---

## 📷 Demo

Coming soon — CLI demo GIF or screen recording.
