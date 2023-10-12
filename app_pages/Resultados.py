import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

def resultados(df_sales):
    '''Results window'''

    st.title("Resultados")

    date_col = list(df_sales['data_venda_abv'])
    df_sales['id_produto'] = df_sales['id_produto'].astype(str)

    with st.container():

        date_selected = st.multiselect('Selecione a(s) Data(s)', date_col)
        if len(date_selected) > 0:
            df_sales_up = pd.DataFrame(columns=df_sales.columns)
            for date in date_selected:
                year_selected = date.split('/')[0]
                month_selected = date.split('/')[1]
                df_temp = df_sales.loc[(df_sales['data_venda'].dt.year == int(year_selected)) & (df_sales['data_venda'].dt.month == int(month_selected))]
                df_sales_up = pd.concat([df_sales_up, df_temp])
        else:
            df_sales_up = df_sales

    # Create DFs
    # df_emp_up = df_sales_up[['id_funcionario','nome_funcionario','valor_venda']].groupby(by=['id_funcionario','nome_funcionario']).sum().sort_values(by='valor_venda', ascending=False).reset_index()
    # df_emp_up_count = df_sales_up[['id_funcionario','nome_funcionario','valor_venda']].groupby(by=['id_funcionario','nome_funcionario']).count().sort_values(by='valor_venda', ascending=False).reset_index()
    # df_emp_up_count.rename(columns={'valor_venda':'qtd'}, inplace=True)

    df_prod_up = df_sales_up[['id_produto','nome_produto','valor_venda']].groupby(by=['id_produto','nome_produto']).sum().sort_values(by='valor_venda', ascending=False).reset_index()
    df_prod_up_count = df_sales_up[['id_produto','nome_produto','valor_venda']].groupby(by=['id_produto','nome_produto']).count().sort_values(by='valor_venda', ascending=False).reset_index()
    df_prod_up_count.rename(columns={'valor_venda':'qtd'}, inplace=True)
    df_prod_up_count['qtd'] = df_prod_up_count['qtd'].astype(int)
    
    # df_comissao = df_sales_up[['id_funcionario','nome_funcionario','valor_comissao']].groupby(by=['id_funcionario','nome_funcionario']).sum().sort_values(by='valor_comissao', ascending=False).reset_index()
    # df_valor_liquido_func = df_sales_up[['id_funcionario','nome_funcionario','valor_liquido']].groupby(by=['id_funcionario','nome_funcionario']).sum().sort_values(by='valor_liquido', ascending=False).reset_index()
    # df_valor_liquido_prod = df_sales_up[['id_produto','nome_produto','valor_liquido']].groupby(by=['id_produto','nome_produto']).sum().sort_values(by='valor_liquido', ascending=False).reset_index()

    # Generate option_menu function
    # selected = option_menu(
    #     menu_title = None,
    #     options = ['Produto','Valor Líquido'],
    #     icons = ['person','box','currency-dollar','currency-dollar'],
    #     menu_icon = 'cast',
    #     orientation = 'horizontal'
    # )

    # Display DFs
    # if selected == 'Funcionário':

    #     with st.container():
    #         st.subheader("Quantidade de Vendas por Funcionário")

    #         col1, col2 = st.columns(2)

    #         with col1:    
    #             st.write(df_emp_up_count)
            
    #         with col2:
    #             st.bar_chart(df_emp_up_count[['id_funcionario','qtd']], x='id_funcionario', y='qtd')

    #     with st.container():
    #         st.subheader("Valor de Venda por Funcionário")

    #         col1, col2 = st.columns(2)

    #         with col1:
    #             st.write(df_emp_up)

    #         with col2:
    #             st.bar_chart(df_emp_up[['id_funcionario','valor_venda']], x='id_funcionario', y='valor_venda')

    #     with st.container():
    #         st.subheader("Valor da Comissão por Funcionário")

    #         col1, col2 = st.columns(2)

    #         with col1:
    #             st.write(df_comissao)
            
    #         with col2:
    #             st.bar_chart(df_comissao, x='id_funcionario', y='valor_comissao')

                
    # if selected == 'Produto':
        
    with st.container():
        st.subheader("Quantidade de Vendas por Produto")

        col1, col2 = st.columns(2)

        with col1:
            st.write(df_prod_up_count)

        with col2:
            st.bar_chart(df_prod_up_count, x='nome_produto', y='qtd', )

    with st.container():
        st.subheader("Valor de Venda por Produto")

        col1, col2 = st.columns(2)

        with col1:
            st.write(df_prod_up)

        with col2:
            st.bar_chart(df_prod_up, x='nome_produto', y='valor_venda')

    # if selected == 'Valor Líquido':

        # with st.container():
        #     st.subheader("Valor Líquido por Funcionário")

        #     col1, col2 = st.columns(2)

        #     with col1:
        #         st.write(df_valor_liquido_func)
            
        #     with col2:
        #         st.bar_chart(df_valor_liquido_func[['id_funcionario','valor_liquido']], x='id_funcionario', y='valor_liquido')

        # with st.container():
        #     st.subheader("Valor Líquido por Produto")

        #     col1, col2 = st.columns(2)

        #     with col1:
        #         st.write(df_valor_liquido_prod)
            
        #     with col2:
        #         st.bar_chart(df_valor_liquido_prod[['id_produto','valor_liquido']], x='id_produto', y='valor_liquido')

    return df_sales
