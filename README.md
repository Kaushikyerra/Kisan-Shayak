# Kisan Sahayak (किसान सहायक)

Farmer-focused platform with:
- **Mobile app foundation** (React Native + Expo + TypeScript)
- **Runnable backend MVP** (FastAPI)

## Mobile app (current scope)
- Expo TypeScript app scaffold
- Auth stack + bottom-tab navigation
- Zustand auth store
- React Native Paper theme setup
- Hindi/English i18n bootstrap
- Starter screens for auth + Home/Fields/Krishi AI/Market/Profile

## Backend API (fully runnable MVP)
A complete FastAPI backend is available in `backend/` with endpoint groups for auth, fields, sensors/devices, market, weather, AI assistant, tasks, and schemes.

### Start backend
```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Run backend tests
```bash
cd backend
pytest -q
```

## Mobile app run
```bash
npm install
npm run start
```
