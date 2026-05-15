
import streamlit as st
import pandas as pd

def show():
    st.header("👥 Группа пользователей (Организация)")
    st.caption("Управление участниками группы")

    # Имитация данных пользователей
    if 'users' not in st.session_state:
        st.session_state.users = [
            {"id": 1, "full_name": "Иванов Иван Иванович", "role": "Администратор", "status": "Активен", "email": "ivanov@don.ru"},
            {"id": 2, "full_name": "Сидорова Анна Петровна", "role": "Оператор", "status": "Активен", "email": "sidorova@don.ru"},
            {"id": 3, "full_name": "Петров Сергей Александрович", "role": "Наблюдатель", "status": "Активен", "email": "petrov@don.ru"},
            {"id": 4, "full_name": "Кузнецова Мария Дмитриевна", "role": "Оператор", "status": "Неактивен", "email": "kuznetsova@don.ru"},
        ]

    users_df = pd.DataFrame(st.session_state.users)

    # Фильтры
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Поиск пользователя", "")
    with col2:
        role_filter = st.selectbox("Роль", ["Все", "Администратор", "Оператор", "Наблюдатель"])

    # Фильтрация
    filtered = users_df.copy()
    if search:
        filtered = filtered[filtered['full_name'].str.contains(search, case=False)]
    if role_filter != "Все":
        filtered = filtered[filtered['role'] == role_filter]

    st.subheader(f"Участники группы — {len(filtered)} человек")
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "full_name": "ФИО",
            "role": "Роль",
            "status": "Статус",
            "email": "Email"
        }
    )

    st.markdown("---")

    # Добавление нового пользователя (только для администратора)
    st.subheader("➕ Добавить нового пользователя")
    with st.form("add_user"):
        col_a, col_b = st.columns(2)
        with col_a:
            new_name = st.text_input("ФИО")
            new_email = st.text_input("Email")
        with col_b:
            new_role = st.selectbox("Роль", ["Оператор", "Наблюдатель"])
            new_status = st.selectbox("Статус", ["Активен", "Неактивен"])
        
        submitted = st.form_submit_button("Добавить в группу")
        if submitted and new_name:
            new_user = {
                "id": len(st.session_state.users) + 1,
                "full_name": new_name,
                "role": new_role,
                "status": new_status,
                "email": new_email or "—"
            }
            st.session_state.users.append(new_user)
            st.success(f"Пользователь {new_name} успешно добавлен!")
            st.rerun()

    # Удаление пользователя
    st.subheader("🗑️ Удалить пользователя")
    user_to_delete = st.selectbox("Выберите пользователя для удаления", 
                                  options=[u["full_name"] for u in st.session_state.users])
    
    if st.button("Удалить пользователя", type="primary"):
        st.session_state.users = [u for u in st.session_state.users if u["full_name"] != user_to_delete]
        st.success(f"Пользователь {user_to_delete} удалён")
        st.rerun()