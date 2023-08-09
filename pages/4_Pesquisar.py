import streamlit as st
import pandas as pd
from datetime import datetime as dt

df_sale = pd.read_excel("sheets/sales.xlsx", converters={'data_venda':dt.date})

st.title("Pesquisar Placa")

placa_carro = st.text_input('Digite a placa')

search_button = st.button('Pesquisar')

if search_button:
    placa_carro = placa_carro.upper()
    df_sale_c = df_sale[df_sale['placa_carro'] == placa_carro]
    nr_registros = len(df_sale_c)

    st.text(f'Esta placa possui {nr_registros} registro(s)')

    st.subheader("Tabela de Registros")

    st.write(df_sale_c)