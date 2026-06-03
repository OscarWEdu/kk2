from fastapi.testclient import TestClient
from app.main import app

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