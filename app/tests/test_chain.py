from app.services.llm_service import SmolLM, ConversationHistory

def test_runnable_history_empty_context():
    history = ConversationHistory(history=[])
    out = history.invoke({"question": "Hello"})

    assert out["context"] == ""
    assert out["question"] == "Hello"