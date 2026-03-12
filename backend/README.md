# Kisan Sahayak Backend (FastAPI)

## Run
```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## Test
```bash
cd backend
pytest -q
```

## Included endpoint groups
- Auth: `/auth/send-otp`, `/auth/verify-otp`, `/auth/resend-otp`, `/auth/profile`
- Fields CRUD: `/fields`, `/fields/{id}`
- Sensors & devices: `/sensors/readings`, `/sensors/latest`, `/devices/status`, `/devices/register`, `/devices/{id}/calibrate`
- Market: `/predict-price`, `/market-prices/trends`, `/mandi-prices`
- Weather: `/weather/current`, `/weather/forecast`, `/weather/alerts`
- AI: `/ai/chat`, `/ai/voice`, `/ai/disease-detect`
- Tasks CRUD: `/tasks`, `/tasks/{id}`
- Schemes: `/schemes`, `/schemes/{id}`, `/schemes/check-eligibility`
- WebSocket demo: `/ws/sensors`

> Note: This MVP uses in-memory data stores for a fully runnable local backend. Swap with Supabase/real services for production.
