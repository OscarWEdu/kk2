from fastapi.testclient import TestClient
from fastapi import UploadFile
from app.main import app
from io import BytesIO

client = TestClient(app)

# Creates a simple csv for the sole purpose of testing
def make_test_csv(): #Wasn't too fond of the idea of storing a csv file for the sole purpose of testing
    csv_text = "col1,col2\n1,2\n3,4\n"
    return csv_text.encode("utf-8")

# TESTS:
def test_endpoint_root():
    response = client.get("/")
    assert response.status_code == 200

def test_endpoint_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_endpoint_data_stats_no_data():
    response = client.get("/data/stats")
    assert response.status_code == 404

def test_endpoint_upload_csv():
    files = {
        "file": ("test.csv", BytesIO(make_test_csv()), "text/csv")
    }
    response = client.post("/data/upload_csv", files=files)
    metadata = response.json()

    assert response.status_code == 200
    assert metadata["num_rows"] == 2
    assert metadata["columns"] == ["col1", "col2"]
    assert "dtypes" in metadata

def test_endpoint_upload_csv_invalid_file():
    files = {
        "file": ("bad.txt", BytesIO(b"Not a csv"), "text/plain")
    }
    response = client.post("/data/upload_csv", files=files)
    assert response.status_code == 400

def test_endpoint_upload_csv_no_file():
    response = client.post("/data/upload_csv", files={})
    assert response.status_code == 422

def test_endpoint_data_stats_no_file():
    response = client.get("/data/stats")
    assert response.status_code == 404

def test_endpoint_data_stats():
    files = {
        "file": ("test.csv", BytesIO(make_test_csv()), "text/csv")
    }
    response = client.post("/data/upload_csv", files=files)
    assert response.status_code == 200

    stats_response = client.get("/data/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()["stats"]
    assert "col1" in stats
    assert "col2" in stats

def test_endpoint_ai_ask(monkeypatch):
    test_answer = "42."
    def mock_invoke(self, input):
        return {"answer": test_answer, **input}

    from app.services.llm_service import SmolLM
    monkeypatch.setattr(SmolLM, "invoke", mock_invoke) # patch invoke

    response = client.post("/ai/ask", json = {"question": "What is the meaning of testing?"})

    assert response.status_code == 200
    assert response.json() == test_answer