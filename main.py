import streamlit as st
import pandas as pd
from config import APP_TITLE, APP_SUBTITLE, SENSORS
from data.sensors import get_all_data
from data.sensors import get_all_data, generate_sensor_data
import plotly.express as px


#состояние датчиков 
if 'sensor_states' not in st.session_state:
    st.session_state.sensor_states = {
        sensor['id']: {
            "status": sensor["status"],
            "mode": "Нормальный",
            "active": True,
            "last_changed": "При запуске"
        } for sensor in SENSORS
    }

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

#настройки системы
if 'unit_system' not in st.session_state:
    st.session_state.unit_system = "Метрическая"

#генерация данных при загрузкке!
if 'all_data' not in st.session_state:
    st.session_state.all_data = get_all_data(rows=300)

#описание боковой панели
st.sidebar.title("🧭 Навигация")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Выберите раздел:",
    ["🏠 Главная", "🗺️ Карта", "📊 Данные датчиков", 
     "👥 Группа пользователей", "📄 Отчеты", "⚙️ Аккаунт"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"**Территория:**\n{APP_SUBTITLE}")

#описание главной страницы
if page == "🏠 Главная":
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    st.markdown("---")

    #настройка систем измерения
    st.subheader("⚙️ Настройки отображения")
    col_set1, col_set2 = st.columns([2, 1])
    
    with col_set1:
        unit_system = st.radio(
            "Система измерения:",
            ["Метрическая (Цельсий, мм)", "Американская (Фаренгейт, дюймы)"],
            horizontal=True,
            key="main_unit"
        )
        st.session_state.unit_system = unit_system

    with col_set2:
        if st.button("🔄 Обновить все данные", type="primary"):
            st.session_state.all_data = get_all_data(rows=300)
            st.success("Данные обновлены!")

    st.markdown("---")

    #получение данных
    df = st.session_state.all_data.copy()
    latest_data = df.groupby('sensor_name').last().reset_index()

    #функция конвертации ед.измерения
    is_imperial = "Американская" in st.session_state.unit_system

    def convert_temp(c):
        return round(c * 1.8 + 32, 1) if is_imperial else c

    def convert_precip(mm):
        return round(mm * 0.03937, 2) if is_imperial else mm

    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_temp = round(convert_temp(latest_data['temperature'].mean()), 1)
        delta_temp = convert_temp(latest_data['temperature'].mean() - 18.5)  #сравнение с нормой
        st.metric(
            label="🌡️ Средняя температура",
            value=f"{avg_temp}°{'F' if is_imperial else 'C'}",
            delta=f"{delta_temp:+.1f}",
            delta_color="normal"
        )

    with col2:
        avg_soil = latest_data['soil_moisture'].mean()
        delta_soil = avg_soil - 45
        st.metric(
            label="💧 Влажность почвы",
            value=f"{avg_soil:.1f}%",
            delta=f"{delta_soil:+.1f}%",
            delta_color="normal"
        )

    with col3:
        avg_hum = latest_data['humidity'].mean()
        delta_hum = avg_hum - 60
        st.metric(
            label="💦 Влажность воздуха",
            value=f"{avg_hum:.1f}%",
            delta=f"{delta_hum:+.1f}%",
            delta_color="normal"
        )

    with col4:
        total_precip = round(convert_precip(latest_data['precipitation'].sum()), 1)
        unit_p = "дюймов" if is_imperial else "мм"
        delta_precip = total_precip - 8 if is_imperial else total_precip - 15 
        st.metric(
            label="🌧️ Суммарные осадки",
            value=f"{total_precip} {unit_p}",
            delta=f"{delta_precip:+.1f}",
            delta_color= "normal"
        )
    # Статус датчиков
    st.subheader("Статус датчиков")
    sensor_status = []
    
    st.markdown("---")
    st.subheader("Статус всех датчиков")

    status_list = []
    for sensor in SENSORS:
        state = st.session_state.sensor_states[sensor['id']]
        status_emoji = "🟢" if state["active"] else "🔴"
        status_list.append({
            "Датчик": sensor["name"],
            "Состояние": f"{status_emoji} {'Активен' if state['active'] else 'Отключён'}",
            "Статус": state["status"].capitalize(),
            "Режим": state["mode"],
            "Последнее изменение": state["last_changed"]
        })

    st.dataframe(pd.DataFrame(status_list), use_container_width=True, hide_index=True)
    

    # График
    st.subheader("📊 Аналитика по датчикам")

    metric_option = st.selectbox(
        "Выберите показатель для отображения:",
        ["Температура", "Влажность почвы", "Влажность воздуха", "Осадки", "Скорость ветра"],
        index=0
    )

    # Конвертация
    display_data = latest_data.copy()
    
    if metric_option == "Температура":
        y_column = "temperature"
        y_label = f"Температура (°{'F' if is_imperial else 'C'})"
        display_data['display_value'] = display_data['temperature'].apply(convert_temp)
        color_scale = "RdYlBu_r"
        
    elif metric_option == "Влажность почвы":
        y_column = "soil_moisture"
        y_label = "Влажность почвы (%)"
        display_data['display_value'] = display_data['soil_moisture']
        color_scale = "BuGn"
        
    elif metric_option == "Влажность воздуха":
        y_column = "humidity"
        y_label = "Влажность воздуха (%)"
        display_data['display_value'] = display_data['humidity']
        color_scale = "Blues"
        
    elif metric_option == "Осадки":
        y_column = "precipitation"
        y_label = f"Осадки ({'дюймов' if is_imperial else 'мм'})"
        display_data['display_value'] = display_data['precipitation'].apply(convert_precip)
        color_scale = "YlGnBu"
        
    elif metric_option == "Скорость ветра":
        y_column = "wind_speed"
        y_label = "Скорость ветра (м/с)"
        display_data['display_value'] = display_data['wind_speed']
        color_scale = "Oranges"

    # Построение диаграммы
    fig = px.bar(
        display_data, 
        x="sensor_name", 
        y="display_value",
        title=f"{metric_option} по датчикам",
        labels={"display_value": y_label, "sensor_name": "Датчик"},
        color="display_value",
        color_continuous_scale=color_scale
    )

    fig.update_layout(
        xaxis_title="Датчики",
        yaxis_title=y_label,
        height=500
    )


#описание боковой панели и функционал
    st.plotly_chart(fig, use_container_width=True)
elif page == "🗺️ Карта":
    from pages.map import show
    show()

elif page == "📊 Данные датчиков":
    from pages.data_sensor import show
    show()

elif page == "👥 Группа пользователей":
    from pages.users import show
    show()

elif page == "📄 Отчеты":
    from pages.reports import show
    show()


elif page == "⚙️ Аккаунт":
    from pages.account import show
    show()