
import streamlit as st
import pandas as pd
from datetime import datetime
from data.sensors import get_all_data

def show():
    st.header("📄 Отчеты и экспорт данных")
    st.caption("Экспорт данных мониторинга")

    df = get_all_data(rows=200)

    st.subheader("📊 Выберите данные для отчета")

    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input("Период", 
                                   [datetime.now().date(), datetime.now().date()])
    with col2:
        sensors_selected = st.multiselect(
            "Выберите датчики",
            options=[s["name"] for s in st.session_state.get("SENSORS", [])] or 
                    [s["name"] for s in __import__("config").SENSORS],
            default=[s["name"] for s in __import__("config").SENSORS]
        )

    # Фильтрация
    filtered = df[df['sensor_name'].isin(sensors_selected)].copy()

    st.subheader(f"Предпросмотр отчета — {len(filtered)} записей")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📥 Экспорт данных")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        if st.button("💾 Экспорт в CSV", use_container_width=True):
            csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Скачать CSV файл",
                data=csv,
                file_name=f"Мониторинг_Дон_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with col_exp2:
        if st.button("📗 Экспорт в Excel", use_container_width=True):
            output = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
            filtered.to_excel(output, index=False, sheet_name='Данные')
            output.close()
            
            with open('temp.xlsx', 'rb') as f:
                excel_data = f.read()
            
            st.download_button(
                label="Скачать Excel файл",
                data=excel_data,
                file_name=f"Мониторинг_Дон_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with col_exp3:
        if st.button("📄 Экспорт в JSON", use_container_width=True):
            json_data = filtered.to_json(orient="records", force_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                label="Скачать JSON",
                data=json_data,
                file_name=f"Мониторинг_Дон_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )

    # Итоговая статистика отчета
    st.markdown("---")
    st.subheader("Итоговая статистика")
    stats_col1, stats_col2 = st.columns(2)
    with stats_col1:
        st.metric("Максимальная температура", f"{filtered['temperature'].max():.1f}°C")
        st.metric("Минимальная влажность почвы", f"{filtered['soil_moisture'].min():.1f}%")
    with stats_col2:
        st.metric("Средняя температура", f"{filtered['temperature'].mean():.1f}°C")
        st.metric("Всего осадков", f"{filtered['precipitation'].sum():.1f} мм")