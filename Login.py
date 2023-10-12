import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from core.db import Db_pg
from app_pages.Home import home
from app_pages.FluxoCaixa import fluxo_caixa
from app_pages.Registrar import registrar
from app_pages.Resultados import resultados
from app_pages.functions import load_data

st.set_page_config(page_title='App', layout='wide')

# User Auth

cur, conn = Db_pg.connect()

query = fr"select * from app_auth;"
cur.execute(query)
list_cred = cur.fetchall()
credentials = {"usernames":{}}
dict_permissions = {}
dict_company_id = {}
for cred in list_cred:
    credentials["usernames"][cred[0]] = {'email':cred[0],'name':cred[1],'password':cred[2]}
    dict_permissions[cred[0]] = cred[3]
    dict_company_id[cred[0]] = cred[6]

Db_pg.disconnect(cur, conn)

col1, col2, col3 = st.columns(3)

with col2:
    authenticator = stauth.Authenticate(credentials, "sales_dashboard", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

if authentication_status:

    company_id = dict_company_id[username]

    if "df_sales" not in st.session_state:
        df_sales, df_employees, df_despesa, df_products = load_data(company_id)
        st.session_state["df_sales"] = df_sales
        st.session_state["df_employees"] = df_employees
        st.session_state["df_despesa"] = df_despesa
        st.session_state["df_products"] = df_products

    else:
        df_sales = st.session_state["df_sales"]
        df_employees = st.session_state["df_employees"]
        df_despesa = st.session_state["df_despesa"]
        df_products = st.session_state["df_products"]

    with st.sidebar:
        selected = option_menu(name, ['Home', 'Registrar','Resultados','Fluxo de Caixa'], menu_icon="cast", default_index=0)
        authenticator.logout('Logout')
    
    cur, conn = Db_pg.connect()

    if selected == 'Home':

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            df_sales = home(cur, conn, df_sales)
            st.session_state["df_sales"] = df_sales

    if selected == 'Registrar':

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            df_employees, df_products, df_sales, df_despesa = registrar(cur, conn, company_id, df_employees, df_products, df_sales, df_despesa)
            st.session_state["df_employees"] = df_employees
            st.session_state["df_products"] = df_products
            st.session_state["df_sales"] = df_sales
            st.session_state["df_despesa"] = df_despesa

    if selected == 'Resultados':

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            df_sales = resultados(df_sales)
            st.session_state["df_sales"] = df_sales

    if selected == 'Fluxo de Caixa':

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            df_sales, df_despesa = fluxo_caixa(df_sales, df_despesa)
            st.session_state["df_sales"] = df_sales
            st.session_state["df_despesa"] = df_despesa

    Db_pg.disconnect(cur, conn)
    