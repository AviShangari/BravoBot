import os
import pytest
from vector_store import VectorStore

TEST_INDEX_PATH = "test_vector_index"

@pytest.fixture
def store():
    # Clean test store
    if os.path.exists(f"{TEST_INDEX_PATH}.faiss"):
        os.remove(f"{TEST_INDEX_PATH}.faiss")
    if os.path.exists(f"{TEST_INDEX_PATH}.pkl"):
        os.remove(f"{TEST_INDEX_PATH}.pkl")

    return VectorStore(index_path=TEST_INDEX_PATH)

def test_add_and_query(store):
    store.add("I love hiking in the mountains")
    result = store.query("What do I enjoy doing?")
    assert isinstance(result, list)
    assert any("hiking" in r.lower() for r in result)

def test_multiple_adds_and_topk(store):
    store.add("I love pizza")
    store.add("I have a dog named Buddy")
    store.add("I enjoy quiet time with books")

    results = store.query("What do I eat?", top_k=2)
    assert len(results) <= 2
    assert any("pizza" in r.lower() for r in results)

def test_delete_and_query(store):
    text = "I love spicy ramen"
    store.add(text)
    assert text in store.texts

    store.delete(text)
    assert text not in store.texts
    assert text not in store.query("ramen")

def test_clear(store):
    store.add("Test sentence one")
    store.add("Test sentence two")
    assert len(store.texts) > 0

    store.clear()
    assert store.texts == []
    assert store.query("anything") == []
