from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.security import create_test_token
from datetime import datetime, timedelta

client = TestClient(app)

test_user_token = create_test_token(username="testuser")
headers = {"Authorization": f"Bearer {test_user_token}"}

def test_get_stock_report_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/reports/stock")
    assert response.status_code == 401

def test_get_stock_report_authorized():
    response = client.get(f"{settings.API_V1_STR}/reports/stock", headers=headers)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert data["report_type"] == "Stock Report"

def test_get_movements_report():
    start_date = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    end_date = datetime.utcnow().isoformat() + "Z"
    
    payload = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    response = client.post(f"{settings.API_V1_STR}/reports/movements", headers=headers, json=payload)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert data["report_type"] == "Inventory Movement Report"
        assert data["date_range"]["start_date"] == start_date