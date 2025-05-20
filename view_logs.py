from session_log import SessionLogger

logger = SessionLogger()

logs = logger.get_full_log(n=100, show_time=True)  # Get last 100 entries
for timestamp, role, text in logs:
    print(f"[{timestamp}] {role.upper()}: {text}")
