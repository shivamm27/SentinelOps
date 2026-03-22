import streamlit as st

def login():

    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")