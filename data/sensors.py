import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from config import SENSORS

def generate_sensor_data(sensor_id: int, base_time=None):
    """Генерирует данные для одного датчика"""
    sensor = next(s for s in SENSORS if s["id"] == sensor_id)
    
    if base_time is None:
        base_time = datetime.now()
    
    time_offset = timedelta(minutes=random.randint(-30, 0))
    timestamp = base_time + time_offset
    
    base_temp = [19, 17, 20, 18, 16, 21, 18.5][sensor_id-1]
    
    return {
        "sensor_id": sensor_id,
        "sensor_name": sensor["name"],
        "timestamp": timestamp.strftime("%d.%m.%Y %H:%M"),
        "temperature": round(np.random.normal(base_temp, 2.5), 1),
        "humidity": round(np.random.uniform(45, 82), 1),
        "soil_moisture": round(np.random.uniform(25, 58), 1),
        "precipitation": round(max(0, np.random.normal(1, 2.5)), 1),
        "wind_speed": round(np.random.uniform(1, 11), 1),
        "battery": random.randint(68, 100),
        "status": sensor["status"]
    }


def get_all_data(rows=120):
    """Генерирует данные для таблицы и графиков"""
    data = []
    base_time = datetime.now()
    
    for sensor in SENSORS:
        for i in range(rows // len(SENSORS) + 3):
            row = generate_sensor_data(sensor["id"], base_time - timedelta(minutes=i*5))
            data.append(row)
    
    df = pd.DataFrame(data)
    return df.sort_values("timestamp", ascending=False).reset_index(drop=True)