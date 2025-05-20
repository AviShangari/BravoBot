from vector_store import VectorStore

vector_mem = VectorStore()

# List current memory
print("Stored vector memories:")
for i, text in enumerate(vector_mem.texts):
    print(f"{i + 1}. {text}")

# Ask user which one to delete
try:
    choice = int(input("\nEnter the number of the memory to delete (or 0 to cancel): "))
    if choice == 0:
        print("Cancelled.")
    elif 1 <= choice <= len(vector_mem.texts):
        text_to_delete = vector_mem.texts[choice - 1]
        confirmed = input(f"Are you sure you want to delete: \"{text_to_delete}\"? (y/n): ").lower()
        if confirmed == "y":
            success = vector_mem.delete(text_to_delete)
            if success:
                print("Memory deleted.")
            else:
                print("Could not delete memory.")
        else:
            print("Cancelled.")
    else:
        print("Invalid choice.")
except ValueError:
    print("Please enter a valid number.")
