APP_TITLE = "Мониторинг Нижнего течения Дона"
APP_SUBTITLE = "Овражно-балочная сеть • Сельскохозяйственный мониторинг"

SENSORS = [
    {"id": 1, "name": "Датчик 1 - Донской",          "lat": 47.52, "lon": 40.15, "status": "active"},
    {"id": 2, "name": "Датчик 2 - Балка 1",           "lat": 47.48, "lon": 40.22, "status": "active"},
    {"id": 3, "name": "Датчик 3 - Сельхозполе А",    "lat": 47.45, "lon": 40.08, "status": "active"},
    {"id": 4, "name": "Датчик 4 - Овраг Центральный","lat": 47.55, "lon": 40.18, "status": "active"},
    {"id": 5, "name": "Датчик 5 - Донская пойма",    "lat": 47.40, "lon": 40.25, "status": "warning"},
    {"id": 6, "name": "Датчик 6 - Балка Южная",      "lat": 47.38, "lon": 40.12, "status": "active"},
    {"id": 7, "name": "Датчик 7 - Поле Экспериментальное", "lat": 47.50, "lon": 40.05, "status": "active"},
]

# Глобальное состояние (будет переопределено в session_state)
DEFAULT_SENSOR_STATES = {
    s["id"]: {
        "status": s["status"],
        "mode": "Нормальный",
        "active": True
    } for s in SENSORS
}