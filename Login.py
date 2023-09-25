import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from st_pages import Page, add_page_title, show_pages
import pandas as pd
from datetime import datetime as dt
import datetime
import pickle
from pathlib import Path
# from core.db import Db_mg, Db_pg
from app_pages.Home import home
from app_pages.FluxoCaixa import fluxo_caixa
from app_pages.Registrar import registrar
from app_pages.Resultados import resultados

st.set_page_config(page_title='App', layout='wide')

# --- USER AUTHENTICATION ---
names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

credentials = {
        "usernames":{
            usernames[0]:{
                "email":'pparker@gmail.com',
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "email":'rmiller@gmail.com',
                "name":names[1],
                "password":hashed_passwords[1]
                }
            }
        }

# cur, conn = Db_pg.connect()

# query = fr"select * from autodemand_auth;"
# cur.execute(query)
# list_cred = cur.fetchall()
# credentials = {"usernames":{}}
# for cred in list_cred:
#     credentials["usernames"][cred[0]] = {'email':cred[0],'name':cred[2],'password':cred[1]}

col1, col2, col3 = st.columns(3)

with col2:
    authenticator = stauth.Authenticate(credentials, "sales_dashboard", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

if authentication_status:
    with st.sidebar:
        selected = option_menu(name, ['Home', 'Registrar','Resultados','Fluxo de Caixa'], menu_icon="cast", default_index=0)
        authenticator.logout('Logout')
    
    if selected == 'Home':
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            home()
    if selected == 'Registrar':
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            registrar()
    if selected == 'Resultados':
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            resultados()
    if selected == 'Fluxo de Caixa':
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            fluxo_caixa()
    