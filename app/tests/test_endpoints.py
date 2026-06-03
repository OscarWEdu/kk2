from fastapi.testclient import TestClient
from fastapi import UploadFile
from app.main import app
from io import BytesIO

# Creates a simple csv for the sole purpose of testing
def make_test_csv(): #Wasn't too fond of the idea of storing a csv file for the sole purpose of testing
    csv_text = "col1,col2\n1,2\n3,4\n"
    return csv_text.encode("utf-8")

client = TestClient(app)

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
    