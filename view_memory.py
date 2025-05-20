from memory import MemoryStore

mem = MemoryStore()
entries = mem.list_all()

for key, value in entries:
    print(f"{key}: {value}")
