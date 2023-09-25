import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import time, datetime as dt

def registrar():
    st.title("Registro de Dados")

    # Uploading sheets
    # df_func = st.cache_data(pd.read_excel)("sheets/employees.xlsx")"C:\despesas.xlsx"
    df_func = pd.read_excel("sheets/employees.xlsx", converters={'cpf': str, 'data_nascimento': dt.date})
    df_prod = pd.read_excel("sheets/products.xlsx")
    df_sale = pd.read_excel("sheets/sales.xlsx", converters={'data_venda': dt.date})
    df_desp = pd.read_excel("sheets/despesas.xlsx", converters={'data_despesa': dt.date})
    # df_func = pd.read_excel("C:/employees.xlsx", converters={'cpf': str, 'data_nascimento': dt.date})
    # df_prod = pd.read_excel("C:/products.xlsx")
    # df_sale = pd.read_excel("C:/sales.xlsx", converters={'data_venda': dt.date})
    # df_desp = pd.read_excel("C:/despesas.xlsx", converters={'data_despesa': dt.date})
    df_sale = df_sale.sort_values('id_venda', ascending=False).reset_index(drop=True)

    selected = option_menu(
        menu_title = None,
        options = ['Venda','Funcionário','Produto','Despesa'],
        icons = ['person','box','currency-dollar'],
        menu_icon = 'cast',
        orientation = 'horizontal',
        default_index = 0
    )

    if selected == 'Venda':
        st.subheader("Registrar Venda")
        with st.form(key="reg_sale", clear_on_submit=True):
            
            id_sale = df_sale['id_venda'].max() + 1 if pd.isna(df_sale['id_venda'].max()) == False else 1
            funcionarios = tuple(df_func['id_funcionario'].map(str) + ' - ' + df_func['nome_funcionario'].map(str))
            produtos = tuple(df_prod['id_produto'].map(str) + ' - ' + df_prod['nome_produto'].map(str))

            id_func_s = st.selectbox('Funcionário', funcionarios)
            id_prod_s = st.selectbox('Produto', produtos)
            placa_carro = st.text_input('Placa do Carro')
            nome_cliente = st.text_input('Nome do Cliente')
            carro_cliente = st.text_input('Carro do Cliente')
            data = st.date_input("Data da Venda")
            hora_venda = st.time_input('Hora da Venda', time(dt.now().hour, dt.now().minute))
            
            submit_prod = st.form_submit_button(label="Salvar")

            if submit_prod:
                func = id_func_s.split(' - ')
                id_funcionario = func[0]
                nome_funcionario = func[1]
                prod = id_prod_s.split(' - ')
                id_produto = prod[0]
                nome_produto = prod[1]
                placa_carro = placa_carro.upper()

                valor_venda = df_prod.loc[df_prod['id_produto'] == int(id_produto), 'valor_venda'].values[0]
                taxa_comissao = df_func.loc[df_func['id_funcionario'] == int(id_funcionario), 'taxa_comissao'].values[0]
                valor_comissao = round(taxa_comissao * valor_venda, 2)
                valor_liquido = valor_venda - valor_comissao

                df_temp_sale = pd.DataFrame([{"id_venda": id_sale, "id_funcionario": id_funcionario, "nome_funcionario": nome_funcionario, "id_produto": id_produto, "nome_produto": nome_produto, "placa_carro": placa_carro,
                                        'nome_cliente': nome_cliente, 'carro_cliente': carro_cliente, "valor_venda": valor_venda, "data_venda": data, "taxa_comissao": taxa_comissao, "valor_comissao": valor_comissao, 
                                        "valor_liquido": valor_liquido, "hora_venda": hora_venda, "finalizado": 0}])
                df_sale = pd.concat([df_temp_sale, df_sale], ignore_index=True)
                df_sale.to_excel("sheets/sales.xlsx", index=False)

                st.success("Venda registrada com sucesso!")

        st.subheader("Deletar Venda")
        with st.form(key="del_sale", clear_on_submit=True):
            
            vendas = list(df_sale['id_venda'].map(str) + ' - ' + df_sale['nome_produto'].map(str))

            id_sale_valid = None
            if 'sb_sale' in st.session_state:
                id_sale_valid = st.session_state['sb_sale']

            id_sale_s = st.selectbox('Venda', vendas, key='sb_sale')
            id_sale_s = id_sale_s if id_sale_s == id_sale_valid else id_sale_valid

            del_sale = st.form_submit_button(label="Deletar")
            
            if del_sale:

                sale = id_sale_s.split(' - ')
                id_venda = int(sale[0])
                nome_produto = sale[1]

                df_sale = df_sale[df_sale['id_venda'] != id_venda]
                df_sale.to_excel("sheets/sales.xlsx", index=False)

                st.success("Venda deletada com sucesso!")

        st.subheader("Tabela Vendas")
        
        st.write(df_sale)

    if selected == 'Funcionário':
        st.subheader("Registrar Funcionário")
        with st.form(key="reg_employee", clear_on_submit=True):

            id_func = df_func['id_funcionario'].max() + 1 if pd.isna(df_func['id_funcionario'].max()) == False else 1
            nome_func = st.text_input("Nome Funcionário", key='nome_func')
            cpf = st.text_input("CPF", key='cpf')
            data_nascimento = st.date_input("Data de Nascimento", key='data_nascimento')
            salario = st.number_input("Salário", key='salario')
            taxa_comissao = st.number_input("Comissão (%)", key='taxa_comissao')

            submit_emp = st.form_submit_button(label="Salvar")
                
            if submit_emp:
                df_temp_func = pd.DataFrame([{"id_funcionario": id_func, "nome_funcionario": nome_func, "cpf": cpf, "data_nascimento": data_nascimento, "salario": salario, "taxa_comissao": taxa_comissao, "emp_validation": True}])
                df_func = pd.concat([df_func, df_temp_func], ignore_index=True)
                df_func.to_excel("sheets/employees.xlsx", index=False)

                st.success("Funcionário registrado com sucesso!")

        st.subheader("Deletar Funcionário")
        with st.form(key="del_employee", clear_on_submit=True):
            
           
            df_func_valid = df_func[df_func['emp_validation'] == True]
            funcionarios = list(df_func_valid['id_funcionario'].map(str) + ' - ' + df_func_valid['nome_funcionario'].map(str))

            id_func_valid = None
            if 'sb_employee' in st.session_state:
                id_func_valid = st.session_state['sb_employee']

            id_func_s = st.selectbox('Funcionário', funcionarios, key='sb_employee')
            id_func_s = id_func_s if id_func_s == id_func_valid else id_func_valid

            del_emp = st.form_submit_button(label="Deletar")
            
            if del_emp:

                func = id_func_s.split(' - ')
                id_funcionario = int(func[0])
                nome_funcionario = func[1]

                df_func.loc[df_func['id_funcionario'] == id_funcionario, 'emp_validation'] = False
                df_func.to_excel("sheets/employees.xlsx", index=False)

                st.success("Funcionário deletado com sucesso!")

        st.subheader("Tabela Funcionários")
        st.write(df_func[df_func['emp_validation'] == True].loc[:, df_func.columns != 'emp_validation'])

    if selected == 'Produto':
        st.subheader("Registrar Produto")
        with st.form(key="reg_product", clear_on_submit=True):

            id_prod = df_prod['id_produto'].max() + 1 if pd.isna(df_prod['id_produto'].max()) == False else 1
            nome_prod = st.text_input("Nome Produto")
            venda_produto = st.number_input("Valor de Venda")

            submit_prod = st.form_submit_button(label="Salvar")

            if submit_prod:
                df_prod = pd.concat([df_prod, pd.DataFrame([{"id_produto": id_prod, "nome_produto": nome_prod, 'valor_venda': venda_produto}])], ignore_index=True)
                df_prod.to_excel("sheets/products.xlsx", index=False)
                st.success("Produto registrado com sucesso!")
        
        st.subheader("Deletar Produto")
        with st.form(key="del_product", clear_on_submit=True):
            
            produtos = list(df_prod['id_produto'].map(str) + ' - ' + df_prod['nome_produto'].map(str))

            id_prod_valid = None
            if 'sb_product' in st.session_state:
                id_prod_valid = st.session_state['sb_product']

            id_prod_s = st.selectbox('Produto', produtos, key='sb_product')
            id_prod_s = id_prod_s if id_prod_s == id_prod_valid else id_prod_valid

            del_prod = st.form_submit_button(label="Deletar")
            
            if del_prod:

                prod = id_prod_s.split(' - ')
                id_produto = int(prod[0])
                nome_produto = prod[1]

                df_prod = df_prod[df_prod['id_produto'] != id_produto]
                df_prod.to_excel("sheets/products.xlsx", index=False)

                st.success("Produto deletado com sucesso!")

        st.subheader("Tabela Produtos")
        st.write(df_prod)

    if selected == 'Despesa':
        st.subheader("Registrar Despesa")
        with st.form(key="despesas", clear_on_submit=True):
            
            id_desp = df_desp['id_despesa'].max() + 1 if pd.isna(df_desp['id_despesa'].max()) == False else 1
            tipo_despesa = st.selectbox('Tipo de Despesa', ['Salário','Material','Conserto'])
            qtd = st.text_input('Quantidade')
            descricao = st.text_input('Descrição')
            valor_despesa = st.number_input('Valor da Despesa')
            data_despesa = st.date_input('Data da Despesa')
            
            submit_desp = st.form_submit_button(label="Salvar")

            if submit_desp:
                qtd = int(qtd)
                df_temp_desp = pd.DataFrame([{'id_despesa': id_desp, 'tipo_despesa': tipo_despesa, 'quantidade': qtd, 'descricao': descricao, 'valor_despesa': valor_despesa, 'data_despesa': data_despesa}])
                df_desp = pd.concat([df_desp, df_temp_desp], ignore_index=True)
                df_desp.to_excel('sheets/despesas.xlsx', index=False)

                st.success("Despesa registrada com sucesso!")

        st.subheader("Deletar Despesa")
        with st.form(key="del_desp", clear_on_submit=True):
            
            despesas = list(df_desp['id_despesa'].map(str) + ' - ' + df_desp['tipo_despesa'].map(str))

            id_desp_valid = None
            if 'sb_desp' in st.session_state:
                id_desp_valid = st.session_state['sb_desp']

            id_desp_s = st.selectbox('Despesa', despesas, key='sb_desp')
            id_desp_s = id_desp_s if id_desp_s == id_desp_valid else id_desp_valid

            del_desp = st.form_submit_button(label="Deletar")
            
            if del_desp:

                desp = id_desp_s.split(' - ')
                id_desp = int(desp[0])
                tipo_despesa = desp[1]

                df_desp = df_desp[df_desp['id_despesa'] != id_desp]
                df_desp.to_excel("sheets/despesas.xlsx", index=False)

                st.success("Despesa deletada com sucesso!")

        st.subheader("Tabela Despesas")
        st.write(df_desp)
