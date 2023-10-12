import streamlit as st
from datetime import datetime as dt
import pandas as pd
from .functions import convert_number

def fluxo_caixa(df_sales, df_despesa):
    st.title('Fluxo de Caixa')

    # df_despesa = pd.read_excel("sheets/despesas.xlsx", converters={'data_despesa':dt.date})
    # df_sales = pd.read_excel("sheets/saless.xlsx", converters={'data_venda':dt.date})

    # df_temp_sales = pd.DataFrame(columns=['id_funcionario','nome_funcionario','id_produto','nome_produto','placa_carro','valor_venda','data_venda','taxa_comissao','valor_comissao','valor_liquido'])
    # df_sales = pd.concat([df_sales, df_temp_sales], ignore_index=True)

    df_sales['data_venda'] = pd.to_datetime(df_sales['data_venda'], format='%Y-%m-%d')
    df_despesa['data_despesa'] = pd.to_datetime(df_despesa['data_despesa'], format='%Y-%m-%d')

    # df_sales['date_col'] = df_sales['data_venda'].map(lambda x: f'{x.year}/{x.month}')
    # df_despesa['date_col'] = df_despesa['data_despesa'].map(lambda x: f'{x.year}/{x.month}')

    date_col_sales = list(set(df_sales['data_venda_abv']))
    date_col_desp = list(set(df_despesa['data_despesa_abv']))
    date_col = list(set(date_col_sales + date_col_desp))
    date_col.sort(reverse=True)

    with st.container():

        # date_validation = False
        date_selected = st.multiselect('Selecione a(s) Data(s)', date_col)

        if len(date_selected) > 0:
            df_sales_up = pd.DataFrame(columns=df_sales.columns)
            for date in date_selected:
                year_selected = date.split('/')[0]
                month_selected = date.split('/')[1]
                df_temp_sales = df_sales.loc[(df_sales['data_venda'].dt.year == int(year_selected)) & (df_sales['data_venda'].dt.month == int(month_selected))]
                df_sales_up = pd.concat([df_sales_up, df_temp_sales])

            df_despesa_up = pd.DataFrame(columns=df_despesa.columns)
            for date in date_selected:
                year_selected = date.split('/')[0]
                month_selected = date.split('/')[1]
                df_temp_desp = df_despesa.loc[(df_despesa['data_despesa'].dt.year == int(year_selected)) & (df_despesa['data_despesa'].dt.month == int(month_selected))]
                df_despesa_up = pd.concat([df_despesa_up, df_temp_desp])

            # date_validation = True

        else:
            df_sales_up = df_sales
            df_despesa_up = df_despesa

    with st.container():

        total_despesas = df_despesa_up['valor_despesa'].sum()
        total_despesas_str = convert_number(total_despesas)
        total_vendas = df_sales_up['valor_venda'].sum()
        total_vendas_str = convert_number(total_vendas)
        # total_comissao = df_sales_up['valor_comissao'].sum()
        # total_comissao_str = convert_number(total_comissao)
        # total_liquido = df_sales_up['valor_liquido'].sum()
        # total_liquido_str = convert_number(total_vendas)
        total_lucro = total_vendas - total_despesas
        total_lucro_str = convert_number(total_lucro)

        st.subheader('Valor de Venda')
        st.write(f'R$ {total_vendas_str}')

        # st.subheader('Valor de Comissão')
        # st.write(f'R$ {total_comissao_str}')

        # st.subheader('Valor Líquido')
        # st.write(f'R$ {total_liquido_str}')

        st.subheader('Despesas')
        st.write(f'R$ {total_despesas_str}')

        st.subheader('Lucro')
        st.write(f'R$ {total_lucro_str}')


    with st.container():

        df_sales_graph = df_sales_up[['data_venda_abv','valor_venda','valor_liquido']].groupby('data_venda_abv').sum().reset_index()
        df_despesa_graph = df_despesa_up[['data_despesa_abv','valor_despesa']].groupby('data_despesa_abv').sum().reset_index()

        df_sales_graph.rename(columns={'data_venda_abv':'data_abv'}, inplace=True)
        df_despesa_graph.rename(columns={'data_despesa_abv':'data_abv'}, inplace=True)

        df_graph = pd.merge(df_sales_graph,df_despesa_graph,how='outer',on='data_abv').reset_index()
        df_graph['lucro'] = df_graph['valor_venda'] - df_graph['valor_despesa']
        
        if len(date_selected) == 1:

            df_graph_bar = df_graph[['valor_venda','valor_despesa','lucro']].T.rename(columns={'0':'Valor'})
            st.bar_chart(df_graph_bar)
        else:
            st.line_chart(df_graph,x='data_abv',y=['valor_venda','valor_despesa','lucro'])

    return df_sales, df_despesa
