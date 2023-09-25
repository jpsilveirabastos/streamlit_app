import streamlit as st
from datetime import datetime as dt
import pandas as pd

def fluxo_caixa():
    st.title('Fluxo de Caixa')

    df_desp = pd.read_excel("sheets/despesas.xlsx", converters={'data_despesa':dt.date})
    df_sale = pd.read_excel("sheets/sales.xlsx", converters={'data_venda':dt.date})

    df_temp_sale = pd.DataFrame(columns=['id_funcionario','nome_funcionario','id_produto','nome_produto','placa_carro','valor_venda','data_venda','taxa_comissao','valor_comissao','valor_liquido'])
    df_sale = pd.concat([df_sale, df_temp_sale], ignore_index=True)

    df_sale['data_venda'] = pd.to_datetime(df_sale['data_venda'], format='%Y-%m-%d')
    df_desp['data_despesa'] = pd.to_datetime(df_desp['data_despesa'], format='%Y-%m-%d')

    df_sale['date_col'] = df_sale['data_venda'].map(lambda x: f'{x.year}/{x.month}')
    df_desp['date_col'] = df_desp['data_despesa'].map(lambda x: f'{x.year}/{x.month}')

    date_col_sale = list(set(df_sale['date_col']))
    date_col_desp = list(set(df_desp['date_col']))
    date_col = list(set(date_col_sale + date_col_desp))
    date_col.sort(reverse=True)

    with st.container():

        # date_validation = False
        date_selected = st.multiselect('Selecione a(s) Data(s)', date_col)

        if len(date_selected) > 0:
            df_sale_up = pd.DataFrame(columns=df_sale.columns)
            for date in date_selected:
                year_selected = date.split('/')[0]
                month_selected = date.split('/')[1]
                df_temp_sale = df_sale.loc[(df_sale['data_venda'].dt.year == int(year_selected)) & (df_sale['data_venda'].dt.month == int(month_selected))]
                df_sale_up = pd.concat([df_sale_up, df_temp_sale])

            df_desp_up = pd.DataFrame(columns=df_desp.columns)
            for date in date_selected:
                year_selected = date.split('/')[0]
                month_selected = date.split('/')[1]
                df_temp_desp = df_desp.loc[(df_desp['data_despesa'].dt.year == int(year_selected)) & (df_desp['data_despesa'].dt.month == int(month_selected))]
                df_desp_up = pd.concat([df_desp_up, df_temp_desp])

            # date_validation = True

        else:
            df_sale_up = df_sale
            df_desp_up = df_desp

    with st.container():

        total_despesas = df_desp_up['valor_despesa'].sum()
        total_vendas = df_sale_up['valor_venda'].sum()
        total_comissao = df_sale_up['valor_comissao'].sum()
        total_liquido = df_sale_up['valor_liquido'].sum()
        total_lucro = total_liquido - total_despesas

        st.subheader('Valor de Venda')
        st.write(f'R$ {total_vendas:,.2f}')

        st.subheader('Valor de Comissão')
        st.write(f'R$ {total_comissao:,.2f}')

        st.subheader('Valor Líquido')
        st.write(f'R$ {total_liquido:,.2f}')

        st.subheader('Despesas')
        st.write(f'R$ {total_despesas:,.2f}')

        st.subheader('Lucro')
        st.write(f'R$ {total_lucro:,.2f}')


    with st.container():

        df_sale_graph = df_sale_up[['date_col','valor_venda','valor_comissao','valor_liquido']].groupby('date_col').sum()
        df_desp_graph = df_desp_up[['date_col','valor_despesa']].groupby('date_col').sum()
        df_graph = pd.merge(df_sale_graph,df_desp_graph,how='outer',on='date_col').reset_index()
        df_graph['lucro'] = df_graph['valor_liquido'] - df_graph['valor_despesa']
        
        if len(date_selected) == 1:

            df_graph_bar = df_graph[['valor_venda','valor_comissao','valor_liquido','valor_despesa','lucro']].T.rename(columns={'0':'Valor'})
            st.bar_chart(df_graph_bar)
        else:
            st.line_chart(df_graph,x='date_col',y=['valor_venda','valor_comissao','valor_liquido','valor_despesa','lucro'])
