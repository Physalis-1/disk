import streamlit as st
import client
import admin
PAGES = {"Гость": client,"Администратор": admin}
st.sidebar.title('Статус')
selection = st.sidebar.radio("кто я?", list(PAGES.keys()))
page = PAGES[selection]
page.app()