from app.services.llm_service import SmolLM, ConversationHistory
from app.models.llm_model import HistoryPair

def test_runnable_history_empty_context():
    history = ConversationHistory(history=[])
    out = history.invoke({"question": "Hello"})

    assert out["context"] == ""
    assert out["question"] == "Hello"

def test_runnable_history():
    history = ConversationHistory(history=[ HistoryPair(user="q1", ai="a1") ])

    out = history.invoke({"question": "some string"})
    assert "User: q1" in out["context"]
    assert "LLM: a1" in out["context"]
