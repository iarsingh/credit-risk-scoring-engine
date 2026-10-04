from fastapi.testclient import TestClient
from credit.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'utilization': 0.9, 'delinquencies': 3, 'income': 25000}).json()["label"]
    high = client.post("/score", json={'utilization': 0.9, 'delinquencies': 3, 'income': 25000}).json()
    low = client.post("/score", json={'utilization': 0.1, 'delinquencies': 0, 'income': 140000}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'utilization': 0.9, 'delinquencies': 3, 'income': 25000})
    body.pop("utilization")
    assert client.post("/score", json=body).status_code == 422
