import streamlit as st
import pandas as pd
from datetime import datetime as dt
from core.config import TESTE_VAR

def home(cur, conn, df_sales):
    st.title('Resumo Geral' + TESTE_VAR)

    # Upload sheets
    # df_func = pd.read_excel("sheets/employees.xlsx", converters={'cpf': str, 'data_nascimento': dt.date})
    # df_prod = pd.read_excel("sheets/products.xlsx")
    # df_sales = pd.read_excel("sheets/sales.xlsx", converters={'data_venda': dt.date})

    df_sales_not_finalized = df_sales[df_sales['finalizado'] == 0][['id_venda','placa_carro','nome_cliente','carro_cliente','data_venda','hora_venda']].reset_index(drop=True)

    df_temp_sale = pd.DataFrame(columns=['id_funcionario','nome_funcionario','id_produto','nome_produto','placa_carro','nome_cliente','carro_cliente','valor_venda','data_venda','hora_venda','taxa_comissao',
                                        'valor_comissao','valor_liquido','finalizado'])
    df_sales = pd.concat([df_sales, df_temp_sale], ignore_index=True)

    df_sales['data_venda'] = pd.to_datetime(df_sales['data_venda'], format='%Y-%m-%d')
    df_sales['data_venda_abv'] = df_sales['data_venda'].map(lambda x: f'{x.year}/{x.month}')
    df_sales_up = df_sales[['data_venda_abv','valor_liquido']].groupby('data_venda_abv').sum()

    date_now = dt.now()
    year_now = date_now.year
    month_now = date_now.month
    df_sales_now = df_sales.loc[(df_sales['data_venda'].dt.year == int(year_now)) & (df_sales['data_venda'].dt.month == int(month_now))]

    with st.container():
        st.header("Pesquisar Placa")

        with st.form(key='search_plate'):
            placa_carro = st.text_input('Digite a placa')

            search_button = st.form_submit_button('Pesquisar')

            if search_button:
                placa_carro = placa_carro.upper()
                df_sales_c = df_sales[df_sales['placa_carro'] == placa_carro]
                nr_registros = len(df_sales_c)

                st.text(f'Esta placa possui {nr_registros} registro(s)')

                st.subheader("Tabela de Registros")

                st.write(df_sales_c)

    with st.container():
        st.header("Vendas em Aberto")

        with st.form(key="open_sales", clear_on_submit=True):
            lista_vendas = []
            for i in range(len(df_sales_not_finalized)):
                lista_vendas.append(f"{df_sales_not_finalized['id_venda'][i]} | {df_sales_not_finalized['placa_carro'][i]} | {df_sales_not_finalized['nome_cliente'][i]} | {df_sales_not_finalized['carro_cliente'][i]} | \
                                    {df_sales_not_finalized['data_venda'][i]} | {df_sales_not_finalized['hora_venda'][i]}")

            # baixa_vendas = st.empty()
            baixa_vendas = st.multiselect('Selecione a(s) venda(s) para dar baixa', lista_vendas)

            upd_sale = st.form_submit_button('Salvar')
            if upd_sale:    
                lista_id_venda = [x.split(' | ')[0] for x in baixa_vendas]  
                for id_venda in lista_id_venda:
                    df_sales.loc[df_sales['id_venda'] == int(id_venda), 'finalizado'] = 1
                
                query = f"UPDATE sales SET finalizado = 1 WHERE id_venda == {id_venda};"
                cur.execute(query)
                conn.commit()

                df_sales_not_finalized = df_sales[df_sales['finalizado'] == 0][['id_venda','placa_carro','data_venda','hora_venda']].reset_index(drop=True)

        st.dataframe(df_sales_not_finalized)

    return df_sales
