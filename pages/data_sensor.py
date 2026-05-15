# pages/3_Данные_датчиков.py
import streamlit as st
import pandas as pd
from data.sensors import generate_sensor_data
from config import SENSORS
import plotly.express as px

def show():
    st.header("📊 Данные датчиков + Управление")
    st.caption("Нижнее течение Дона — 7 датчиков")

    # Инициализация состояния датчиков (один раз)
    if 'sensor_states' not in st.session_state:
        st.session_state.sensor_states = {
            sensor['id']: {
                "status": sensor["status"],
                "mode": "Нормальный",
                "active": True,
                "last_changed": "При запуске"
            } for sensor in SENSORS
        }

    # ====================== ВКЛАДКИ ======================
    tab1, tab2 = st.tabs(["📋 Просмотр данных", "⚙️ Управление датчиками"])

    # ====================== ВКЛАДКА 1: ПРОСМОТР ======================
    with tab1:
        # Фильтрация только активных датчиков
        active_sensors = [s for s in SENSORS if st.session_state.sensor_states[s['id']]['active']]
        
        df = pd.DataFrame([generate_sensor_data(s['id']) for s in active_sensors])
        
        st.subheader(f"Активных датчиков: {len(active_sensors)} / 7")
        
        search = st.text_input("🔍 Поиск", "")
        if search:
            df = df[df['sensor_name'].str.contains(search, case=False)]

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Графики
        st.subheader("📈 Графики")
        metric_choice = st.selectbox("Показатель", 
                                    ["temperature", "soil_moisture", "humidity", "precipitation"])
        fig = px.line(df, x="timestamp", y=metric_choice, color="sensor_name", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ====================== ВКЛАДКА 2: УПРАВЛЕНИЕ ======================
    with tab2:
        st.subheader("⚙️ Управление устройствами")

        for sensor in SENSORS:
            state = st.session_state.sensor_states[sensor['id']]
            
            with st.expander(f"🔧 {sensor['name']} (ID: {sensor['id']})", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 2])

                with col1:
                    active = st.checkbox("Активен", value=state["active"], key=f"active_{sensor['id']}")
                    state["active"] = active

                with col2:
                    new_status = st.selectbox(
                        "Статус",
                        ["active", "warning", "inactive"],
                        index=["active", "warning", "inactive"].index(state["status"]),
                        key=f"status_{sensor['id']}"
                    )
                    state["status"] = new_status

                with col3:
                    new_mode = st.selectbox(
                        "Режим работы",
                        ["Нормальный", "Экономичный", "Интенсивный"],
                        index=["Нормальный", "Экономичный", "Интенсивный"].index(state["mode"]),
                        key=f"mode_{sensor['id']}"
                    )
                    state["mode"] = new_mode

                # Применить изменения
                if st.button("💾 Сохранить изменения", key=f"save_{sensor['id']}"):
                    state["last_changed"] = "Только что"
                    st.success(f"✅ Изменения для {sensor['name']} сохранены!")
                    st.rerun()

                # Информация
                data = generate_sensor_data(sensor['id'])
                st.write(f"**Последние показания:** {data['temperature']}°C | Почва: {data['soil_moisture']}% | Заряд: {data['battery']}%")
                st.caption(f"Последнее изменение: {state['last_changed']}")

                # Кнопка деактивации
                if st.button("🛑 Деактивировать датчик", type="secondary", key=f"deact_{sensor['id']}"):
                    state["active"] = False
                    st.error(f"Датчик {sensor['name']} деактивирован")
                    st.rerun()