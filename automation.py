import webbrowser
import subprocess
import datetime
import os
import requests
from dotenv import load_dotenv
import urllib.parse

class Automation:
    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")

    def google_search(self, query):
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def open_browser(self):
        webbrowser.open("https://www.google.com")

    def tell_time(self):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def search_youtube(self, query):
        encoded_query = urllib.parse.quote_plus(query)
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

                return f"The current temperature in {city} is {temp}°C with {condition}. {precip_msg}"

            else:
                return "Sorry, I couldn't fetch the weather right now."

        except Exception as e:
            print("Weather error:", e)
            return "Something went wrong while checking the weather."


# Example usage:
if __name__ == "__main__":
    auto = Automation()
    auto.open_youtube()
    auto.google_search("how to use whisper with python")
    print(auto.tell_time())
