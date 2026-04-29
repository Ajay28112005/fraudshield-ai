from fastapi import APIRouter
from api.routes.transactions import processor

router = APIRouter()

@router.get("/")
def get_alerts():
    alerts = processor.alert_system.get_alerts()
    return {"alerts": alerts, "total": len(alerts)}

@router.get("/stats")
def get_alert_stats():
    return processor.alert_system.get_stats()