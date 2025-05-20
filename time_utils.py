import dateparser
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone("America/Toronto")

def get_time_range_from_phrase(phrase):
    now = datetime.now(tz)
    phrase = phrase.lower().strip()

    # Controlled time phrases
    if "last hour" in phrase:
        end = now
        start = end - timedelta(hours=1)
        return start, end

    if "yesterday" in phrase and "afternoon" not in phrase:
        y = now - timedelta(days=1)
        start = y.replace(hour=0, minute=0, second=0, microsecond=0)
        end = y.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start, end

    if "this morning" in phrase or "today morning" in phrase:
        start = now.replace(hour=6, minute=0, second=0, microsecond=0)
        end = now.replace(hour=12, minute=0, second=0, microsecond=0)
        return start, end

    if "this afternoon" in phrase or "today afternoon" in phrase:
        start = now.replace(hour=12, minute=0, second=0, microsecond=0)
        end = now.replace(hour=17, minute=0, second=0, microsecond=0)
        return start, end

    if "this evening" in phrase or "today evening" in phrase:
        start = now.replace(hour=17, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start, end

    if "today" in phrase:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
        return start, end

    # Fallback: Specific dates like "May 15"
    parsed = dateparser.parse(
        phrase,
        settings={
            'TIMEZONE': 'America/Toronto',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'PREFER_DATES_FROM': 'past'
        }
    )

    if not parsed:
        return None, None

    start = parsed.replace(hour=0, minute=0, second=0, microsecond=0)
    end = parsed.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start, end

if __name__ == "__main__":
    from time_utils import get_time_range_from_phrase

    test_phrases = [
        "last hour",
        "yesterday",
        "today",
        "this morning",
        "this afternoon",
        "this evening",
        "today morning",
        "today afternoon",
        "today evening",
        "May 14",
        "may 1",
        "June 10 2023"
    ]

    for phrase in test_phrases:
        print(f"\nTesting phrase: '{phrase}'")
        start, end = get_time_range_from_phrase(phrase)
        if start and end:
            print("Start:", start.strftime("%Y-%m-%d %I:%M %p"))
            print("End:  ", end.strftime("%Y-%m-%d %I:%M %p"))
        else:
            print("Could not parse time range.")
