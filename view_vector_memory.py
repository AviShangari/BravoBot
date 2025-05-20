from vector_store import VectorStore

vector_mem = VectorStore()

print("Vector Memory Contents:")
for i, text in enumerate(vector_mem.texts):
    print(f"{i + 1}. {text}")
