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


def test_runnable_smollm(monkeypatch):
    test_answer = "42."

    original_init = SmolLM.__init__
    # call Pydantic's init but mock the SmolLM init
    def mock_init(self):
        original_init(self)
        self.pipe = None

    def mock_invoke(self, input):
        return {"answer": test_answer, **input}

    monkeypatch.setattr(SmolLM, "__init__", mock_init)
    monkeypatch.setattr(SmolLM, "invoke", mock_invoke)
    llm = SmolLM()
    result = llm.invoke({"prompt": "What is the meaning of testing?", "context": ""})

    assert result["answer"] == test_answer
