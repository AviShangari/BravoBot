import webbrowser
import subprocess
import datetime
import os
import requests
from dotenv import load_dotenv
import urllib.parse
import csv
from llm import LLMInterface

class Automation:
    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        print("BravoBot: Opening YouTube...")

    def google_search(self, query):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        print(f"Bravobot: Searching Google for: {query}")

    def open_browser(self):
        webbrowser.open("https://www.google.com")
        print("BravoBot: Opening Google Chrome browser...")

    def tell_time(self):
        now = datetime.datetime.now()
        print(f"Bravobot: The current time is {now.strftime('%I:%M %p')}")
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def search_youtube(self, query):
        encoded_query = urllib.parse.quote_plus(query)
        print(f"Bravobot: Searching youtube for: {query}")
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        webbrowser.open(url)
    
    def get_weather(self):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        city = "Toronto"  # Or detect from IP later
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("main") and data.get("weather"):
                temp = data["main"]["temp"]
                condition = data["weather"][0]["description"]
                main_condition = data["weather"][0]["main"].lower()

                # Precipitation check
                if "rain" in main_condition:
                    precip_msg = "It looks like it's raining today."
                elif "snow" in main_condition:
                    precip_msg = "There may be snow today."
                else:
                    precip_msg = "No precipitation expected today."

                print(f"Bravobot: The current temperature in {city} is {temp}°C with {condition}. {precip_msg}")
                return f"The current temperature in {city} is {temp}°C with {condition}. {precip_msg}"

            else:
                print("Bravobot: Sorry, I couldn't fetch the weather right now.")
                return "Sorry, I couldn't fetch the weather right now."

        except Exception as e:
            print("Weather error:", e)
            return "Something went wrong while checking the weather."
    
    def take_note(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = text.strip()
        with open("notes.csv", mode="a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, note])
        print(f"Bravobot: Saved note: {note}")

    def summarize_last_note(self):
        try:
            with open("notes.csv", mode="r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
                if not rows:
                    return "There are no notes to summarize."
                last_note = rows[-1][1]
        except FileNotFoundError:
            return "You don't have any notes yet."

        llm = LLMInterface()
        prompt = f"Summarize this note: {last_note}"
        summary = llm.ask(prompt)
        return f"Summary: {summary}"

    def list_notes(self, limit=3):
        try:
            with open("notes.csv", mode="r", encoding="utf-8") as f:
                rows = list(csv.reader(f))[-limit:]
                if not rows:
                    return "You have no saved notes."
        except FileNotFoundError:
            return "You haven't taken any notes yet."

        result = [f"{i+1}. {row[1]}" for i, row in enumerate(rows)]
        return "Here are your recent notes:\n" + "\n".join(result)


# Example usage:
if __name__ == "__main__":
    auto = Automation()
    auto.open_youtube()
    auto.google_search("how to use whisper with python")
    print(auto.tell_time())
