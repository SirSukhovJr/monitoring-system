import streamlit as st

def show():
    st.header("⚙️ Аккаунт пользователя")
    st.caption("Управление аккаунтом и настройками")

    # Информация о пользователе
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("👤 Профиль")
        st.write("**ФИО:** Сухов Дмитрий Андреевич")
        st.write("**Роль:** Администратор")
        st.write("**Организация:** Нижнее течение Дона")
        st.write("**Email:** sukhov.d@don-monitoring.ru")

    with col2:
        st.subheader("Статус аккаунта")
        st.success("● Активен")
        st.write("**Последний вход:** Только что")
        st.write("**Дата регистрации:** 15.02.2026")

    st.markdown("---")
