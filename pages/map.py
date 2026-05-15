import streamlit as st
import folium
from streamlit_folium import st_folium
from config import SENSORS
from data.sensors import generate_sensor_data

def show():
    st.header("🗺️ Интерактивная карта Нижнего течения Дона")
    st.caption("Расположение 7 датчиков мониторинга")

    if st.button("🔄 Обновить данные на карте"):
        st.rerun()

    m = folium.Map(location=[47.45, 40.70], zoom_start=10, tiles="OpenStreetMap")

    for sensor in SENSORS:
        state = st.session_state.sensor_states[sensor['id']]
        if not state["active"]:
            continue  # пропускаем отключенные датчики

        data = generate_sensor_data(sensor["id"])
        color = "green" if state["status"] == "active" else "orange"
        
        popup_html = f"""
        <b>{sensor['name']}</b><br>
        📍 Координаты: {sensor['lat']}, {sensor['lon']}<br><br>
        🌡️ Температура: <b>{data['temperature']}°C</b><br>
        💧 Влажность почвы: <b>{data['soil_moisture']}%</b><br>
        🌧️ Осадки: <b>{data['precipitation']} мм</b><br>
        💨 Ветер: <b>{data['wind_speed']} м/с</b><br>
        🔋 Заряд: <b>{data['battery']}%</b>
        """
        
        folium.Marker(
            location=[sensor["lat"], sensor["lon"]],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=sensor["name"],
            icon=folium.Icon(color=color, icon="cloud", prefix="fa")
        ).add_to(m)


    map_data = st_folium(m, width=1400, height=650, returned_objects=[])

    st.info("💡 Нажмите кнопку «Обновить данные на карте», чтобы получить свежие показания.")