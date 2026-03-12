from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_health():
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json()['status'] == 'ok'


def test_auth_profile_and_fields_flow():
    phone = '9876543210'
    send = client.post('/auth/send-otp', json={'phone': phone})
    assert send.status_code == 200

    verify = client.post('/auth/verify-otp', json={'phone': phone, 'otp': '123456'})
    assert verify.status_code == 200
    token = verify.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    profile = client.get('/auth/profile', headers=headers)
    assert profile.status_code == 200
    assert profile.json()['phone'] == phone

    field = client.post(
        '/fields',
        json={'name': 'North Plot', 'crop_type': 'Wheat', 'area_acres': 2.0, 'planting_date': '2026-01-01'},
        headers=headers,
    )
    assert field.status_code == 200
    field_id = field.json()['id']

    fetched = client.get(f'/fields/{field_id}', headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()['name'] == 'North Plot'


def test_market_weather_ai_schemes():
    assert client.get('/mandi-prices').status_code == 200
    assert client.get('/weather/current').status_code == 200
    chat = client.post('/ai/chat', json={'message': 'Irrigation advice', 'language': 'en'})
    assert chat.status_code == 200
    assert 'response' in chat.json()

    schemes = client.get('/schemes')
    assert schemes.status_code == 200
    assert len(schemes.json()) >= 1
