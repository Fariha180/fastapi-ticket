import sys
from pathlib import Path

# Ensure Python can find main.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import api

client = TestClient(api)


def test_index():
    """Check welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    """Add one ticket"""
    payload = {
        "id": 1,
        "flight_name": "Air BD",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka",
    }
    response = client.post("/ticket", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["destination"] == "Dhaka"


def test_get_tickets():
    """Retrieve list of tickets"""
    response = client.get("/ticket")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 1


def test_update_ticket():
    """Update an existing ticket"""
    updated = {
        "id": 1,
        "flight_name": "Air BD Updated",
        "flight_date": "2025-11-20",
        "flight_time": "18:00",
        "destination": "Chittagong",
    }
    response = client.put("/ticket/1", json=updated)
    assert response.status_code == 200
    assert response.json()["flight_name"] == "Air BD Updated"


def test_delete_ticket():
    """Delete a ticket"""
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
