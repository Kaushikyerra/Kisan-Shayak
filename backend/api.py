from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Kisan Sahayak API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# In-memory stores for MVP
otp_store: dict[str, str] = {}
token_store: dict[str, str] = {}
profiles: dict[str, dict[str, Any]] = {}
fields_store: dict[str, list[dict[str, Any]]] = {}
tasks_store: dict[str, list[dict[str, Any]]] = {}
registered_devices: dict[str, dict[str, Any]] = {}


class OTPRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=15)


class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str = Field(min_length=4, max_length=6)


class ProfileUpdate(BaseModel):
    name: str
    primary_language: str = "hi"
    primary_crop: str = "Wheat"
    location: str = "India"


class FieldIn(BaseModel):
    name: str
    crop_type: str
    area_acres: float
    planting_date: str


class DeviceRegister(BaseModel):
    device_id: str
    sensor_type: str
    field_id: str | None = None


class CalibrateRequest(BaseModel):
    calibration_factor: float = 1.0


class AIChatRequest(BaseModel):
    message: str
    language: str = "hi"


class TaskIn(BaseModel):
    title: str
    field_id: str | None = None
    due_at: str
    priority: str = "medium"


class EligibilityRequest(BaseModel):
    land_acres: float
    crop_type: str
    annual_income: float


def require_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.replace("Bearer ", "", 1)
    phone = token_store.get(token)
    if not phone:
        raise HTTPException(status_code=401, detail="Invalid token")
    return phone


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": now_iso()}


# Authentication
@app.post("/auth/send-otp")
def send_otp(payload: OTPRequest) -> dict[str, Any]:
    otp = "123456"
    otp_store[payload.phone] = otp
    return {"success": True, "phone": payload.phone, "expires_in": 60, "otp_dev_only": otp}


@app.post("/auth/verify-otp")
def verify_otp(payload: OTPVerifyRequest) -> dict[str, Any]:
    saved = otp_store.get(payload.phone)
    if saved != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    token = str(uuid4())
    token_store[token] = payload.phone

    if payload.phone not in profiles:
        profiles[payload.phone] = {
            "name": "Farmer",
            "primary_language": "hi",
            "primary_crop": "Wheat",
            "location": "India",
            "phone": payload.phone,
            "created_at": now_iso(),
        }

    return {"success": True, "access_token": token, "token_type": "bearer", "profile": profiles[payload.phone]}


@app.post("/auth/resend-otp")
def resend_otp(payload: OTPRequest) -> dict[str, Any]:
    return send_otp(payload)


@app.get("/auth/profile")
def get_profile(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    return profiles[phone]


@app.put("/auth/profile")
def update_profile(payload: ProfileUpdate, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    current = profiles.get(phone, {})
    current.update(payload.model_dump())
    current["phone"] = phone
    current["updated_at"] = now_iso()
    profiles[phone] = current
    return current


# Fields
@app.get("/fields")
def get_fields(authorization: str | None = Header(default=None)) -> list[dict[str, Any]]:
    phone = require_token(authorization)
    return fields_store.get(phone, [])


@app.post("/fields")
def create_field(payload: FieldIn, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    field = payload.model_dump()
    field["id"] = str(uuid4())
    field["created_at"] = now_iso()
    fields_store.setdefault(phone, []).append(field)
    return field


@app.get("/fields/{field_id}")
def get_field(field_id: str, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    for field in fields_store.get(phone, []):
        if field["id"] == field_id:
            return field
    raise HTTPException(status_code=404, detail="Field not found")


@app.put("/fields/{field_id}")
def update_field(field_id: str, payload: FieldIn, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    items = fields_store.get(phone, [])
    for idx, field in enumerate(items):
        if field["id"] == field_id:
            updated = payload.model_dump()
            updated.update({"id": field_id, "updated_at": now_iso()})
            items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Field not found")


@app.delete("/fields/{field_id}")
def delete_field(field_id: str, authorization: str | None = Header(default=None)) -> dict[str, bool]:
    phone = require_token(authorization)
    items = fields_store.get(phone, [])
    start_len = len(items)
    fields_store[phone] = [x for x in items if x["id"] != field_id]
    if len(fields_store[phone]) == start_len:
        raise HTTPException(status_code=404, detail="Field not found")
    return {"success": True}


# Sensors / devices
@app.get("/sensors/readings")
def sensor_readings(field_id: str | None = Query(default=None)) -> list[dict[str, Any]]:
    readings = [
        {"sensor_id": "soil-1", "type": "soil_moisture", "value": 42.3, "unit": "%", "field_id": "demo", "timestamp": now_iso()},
        {"sensor_id": "temp-1", "type": "temperature", "value": 29.7, "unit": "°C", "field_id": "demo", "timestamp": now_iso()},
    ]
    if field_id:
        return [r for r in readings if r["field_id"] == field_id]
    return readings


@app.get("/sensors/latest")
def sensors_latest() -> dict[str, Any]:
    return {"data": sensor_readings(), "updated_at": now_iso()}


@app.get("/devices/status")
def devices_status() -> list[dict[str, Any]]:
    if not registered_devices:
        return [{"device_id": "demo-device", "status": "online", "battery": 87, "last_seen": now_iso()}]
    return list(registered_devices.values())


@app.post("/devices/register")
def register_device(payload: DeviceRegister) -> dict[str, Any]:
    data = payload.model_dump()
    data.update({"status": "online", "battery": 100, "last_seen": now_iso()})
    registered_devices[payload.device_id] = data
    return data


@app.put("/devices/{device_id}/calibrate")
def calibrate_device(device_id: str, payload: CalibrateRequest) -> dict[str, Any]:
    device = registered_devices.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device["calibration_factor"] = payload.calibration_factor
    device["calibrated_at"] = now_iso()
    return device


# Market
@app.post("/predict-price")
def predict_price(crop: str = Query("Wheat")) -> dict[str, Any]:
    base = 2300 if crop.lower() == "wheat" else 4500
    predictions = []
    for i in range(1, 8):
        predictions.append({"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"), "price": base + i * 18})
    return {"crop": crop, "predictions": predictions, "confidence": 0.79}


@app.get("/market-prices/trends")
def market_trends(crop: str = Query("Wheat"), days: int = Query(7, ge=7, le=90)) -> dict[str, Any]:
    points = []
    for i in range(days):
        points.append({"day": i + 1, "price": 2000 + i * 10})
    return {"crop": crop, "days": days, "trend": points}


@app.get("/mandi-prices")
def mandi_prices(crop: str = Query("Wheat")) -> list[dict[str, Any]]:
    return [
        {"crop": crop, "market": "Indore Mandi", "modal_price": 2350, "min_price": 2200, "max_price": 2480, "updated_at": now_iso()},
        {"crop": crop, "market": "Bhopal Mandi", "modal_price": 2325, "min_price": 2180, "max_price": 2450, "updated_at": now_iso()},
    ]


# Weather
@app.get("/weather/current")
def weather_current(city: str = Query("Bhopal")) -> dict[str, Any]:
    return {
        "city": city,
        "temperature_c": 29,
        "condition": "Sunny",
        "humidity": 54,
        "wind_kph": 11,
        "pressure_hpa": 1008,
        "updated_at": now_iso(),
    }


@app.get("/weather/forecast")
def weather_forecast(city: str = Query("Bhopal")) -> list[dict[str, Any]]:
    return [
        {"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"), "high": 32 + i % 2, "low": 20 + i % 2, "rain_probability": 20 + i * 5}
        for i in range(7)
    ]


@app.get("/weather/alerts")
def weather_alerts(city: str = Query("Bhopal")) -> list[dict[str, Any]]:
    return [{"city": city, "level": "info", "message": "No severe weather alerts", "timestamp": now_iso()}]


# AI assistant
@app.post("/ai/chat")
def ai_chat(payload: AIChatRequest) -> dict[str, Any]:
    reply = (
        "सिंचाई सुबह या शाम करें, मिट्टी की नमी 35% से कम होने पर पानी दें।"
        if payload.language == "hi"
        else "Irrigate in the morning/evening and water when soil moisture drops below 35%."
    )
    return {"response": reply, "topic": "crop_advisory", "timestamp": now_iso()}


@app.post("/ai/voice")
def ai_voice() -> dict[str, Any]:
    return {"text": "यह वॉइस इनपुट का डेमो रिस्पॉन्स है।", "language": "hi", "timestamp": now_iso()}


@app.post("/ai/disease-detect")
def ai_disease_detect() -> dict[str, Any]:
    return {
        "disease": "Leaf Blight",
        "confidence": 0.88,
        "severity": "Moderate",
        "recommendation": "Use copper-based fungicide and improve drainage.",
        "timestamp": now_iso(),
    }


# Tasks
@app.get("/tasks")
def get_tasks(authorization: str | None = Header(default=None)) -> list[dict[str, Any]]:
    phone = require_token(authorization)
    return tasks_store.get(phone, [])


@app.post("/tasks")
def create_task(payload: TaskIn, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    task = payload.model_dump()
    task.update({"id": str(uuid4()), "status": "pending", "created_at": now_iso()})
    tasks_store.setdefault(phone, []).append(task)
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskIn, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    phone = require_token(authorization)
    items = tasks_store.get(phone, [])
    for idx, task in enumerate(items):
        if task["id"] == task_id:
            updated = payload.model_dump()
            updated.update({"id": task_id, "status": task.get("status", "pending"), "updated_at": now_iso()})
            items[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, authorization: str | None = Header(default=None)) -> dict[str, bool]:
    phone = require_token(authorization)
    items = tasks_store.get(phone, [])
    start_len = len(items)
    tasks_store[phone] = [x for x in items if x["id"] != task_id]
    if len(tasks_store[phone]) == start_len:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}


# Schemes
@app.get("/schemes")
def list_schemes() -> list[dict[str, Any]]:
    return [
        {"id": "pm-kisan", "name": "PM-KISAN", "benefit_amount": 6000, "category": "income-support", "deadline": "rolling"},
        {"id": "pmfby", "name": "PMFBY", "benefit_amount": 0, "category": "insurance", "deadline": "seasonal"},
    ]


@app.get("/schemes/{scheme_id}")
def scheme_details(scheme_id: str) -> dict[str, Any]:
    for scheme in list_schemes():
        if scheme["id"] == scheme_id:
            return {**scheme, "eligibility": ["Indian farmer", "Valid bank account"], "documents": ["Aadhaar", "Land record"]}
    raise HTTPException(status_code=404, detail="Scheme not found")


@app.post("/schemes/check-eligibility")
def check_eligibility(payload: EligibilityRequest) -> dict[str, Any]:
    eligible = payload.land_acres > 0 and payload.annual_income < 500000
    return {"eligible": eligible, "recommended": ["pm-kisan", "pmfby"] if eligible else []}


# Realtime WebSocket for sensor updates (demo stream)
@app.websocket('/ws/sensors')
async def ws_sensors(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            message = {
                "sensor_id": "soil-1",
                "value": 40 + (datetime.now().second % 10),
                "unit": "%",
                "timestamp": now_iso(),
            }
            await websocket.send_json(message)
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
