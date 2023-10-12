import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import time, datetime as dt
import os
from core.db import Db_pg

def on_click_sub(id_funcionario, df_employees, cur, conn):
    '''Delete employee from database'''

    df_employees.loc[df_employees['id_funcionario'] == id_funcionario, 'emp_validation'] = False
    
    query = f"DELETE FROM employees WHERE id_funcionario = {id_funcionario};"
    cur.execute(query)
    conn.commit()

def save_table(table_name: str, df):
    '''Save table in Downloads file'''

    file_path = os.path.expanduser("~") + "\\Downloads"
    file_path = file_path.replace('"','')

    if (file_path[-1] == '/') or (file_path[-1] == '\\'):
        file_path = file_path[:-1]

    df.to_excel(fr"{file_path}/{table_name}_{dt.now().date()}.xlsx", index=False)

def registrar(cur, conn, company_id, df_employees, df_products, df_sales, df_despesa):

    st.title("Registro de Dados")

    if cur.closed:
        cur, conn = Db_pg.connect()

    df_sales = df_sales.sort_values('id_venda', ascending=False).reset_index(drop=True)

    selected = option_menu(
        menu_title = None,
        options = ['Venda','Funcionário','Produto','Despesa'],
        icons = ['currency-dollar','person','box'],
        menu_icon = 'cast',
        orientation = 'horizontal',
        default_index = 0
    )

    if selected == 'Venda':
        st.subheader("Registrar Venda")
        with st.form(key="reg_sales", clear_on_submit=True):
            
            id_sales_atual = df_sales['id_venda'].max()
            if pd.isna(id_sales_atual) == False:
                id_sales = int(id_sales_atual) + 1
            else:
                id_sales = 1

            # funcionarios = tuple(df_employees['id_funcionario'].map(str) + ' - ' + df_employees['nome_funcionario'].map(str))
            produtos = tuple(df_products['id_produto'].map(str) + ' - ' + df_products['nome_produto'].map(str))

            # id_func_s = st.selectbox('Funcionário', funcionarios)
            id_prod_s = st.selectbox('Produto', produtos)
            placa_carro = st.text_input('Placa do Carro')
            nome_cliente = st.text_input('Nome do Cliente')
            carro_cliente = st.text_input('Carro do Cliente')
            data = st.date_input("Data da Venda", format= "DD/MM/YYYY")
            hora_venda = st.time_input('Hora da Venda', time(dt.now().hour, dt.now().minute))
            
            submit_prod = st.form_submit_button(label="Salvar")

            if submit_prod:
                # func = id_func_s.split(' - ')
                # id_funcionario = func[0]
                # nome_funcionario = func[1]
                prod = id_prod_s.split(' - ')
                id_produto = prod[0]
                nome_produto = prod[1]
                placa_carro = placa_carro.upper()
                data_venda_abv = f'{data.year}/{data.month}'

                valor_venda = float(df_products.loc[df_products['id_produto'] == int(id_produto), 'valor_venda'].values[0])
                # taxa_comissao = df_employees.loc[df_employees['id_funcionario'] == int(id_funcionario), 'taxa_comissao'].values[0]
                # valor_comissao = round(taxa_comissao * valor_venda, 2)
                valor_liquido = valor_venda

                df_temp_sales = pd.DataFrame([{"id_venda": id_sales, "id_produto": id_produto, "nome_produto": nome_produto, "placa_carro": placa_carro,
                                        'nome_cliente': nome_cliente, 'carro_cliente': carro_cliente, "valor_venda": valor_venda, "data_venda": data, 
                                        "valor_liquido": valor_liquido, "hora_venda": hora_venda, "finalizado": 0, "data_venda_abv": data_venda_abv}])
                df_sales = pd.concat([df_temp_sales, df_sales], ignore_index=True)
                
                query = f"INSERT INTO sales (id_venda, id_produto, nome_produto, placa_carro, nome_cliente, carro_cliente, valor_venda, data_venda, \
                valor_liquido, hora_venda, finalizado, data_venda_abv, company_id) VALUES ({id_sales}, {id_produto}, '{nome_produto}', '{placa_carro}', '{nome_cliente}', '{carro_cliente}', \
                    {valor_venda}, '{data}', {valor_liquido}, '{hora_venda}', 0, '{data_venda_abv}', '{company_id}');"
                cur.execute(query)
                conn.commit()

                st.success("Venda registrada com sucesso!")

        st.subheader("Deletar Venda")
        with st.form(key="del_sales", clear_on_submit=True):
            
            vendas = list(df_sales['id_venda'].map(str) + ' - ' + df_sales['nome_produto'].map(str))

            id_sales_valid = None
            if 'sb_sales' in st.session_state:
                id_sales_valid = st.session_state['sb_sales']

            id_sales_s = st.selectbox('Venda', vendas, key='sb_sales')
            id_sales_s = id_sales_s if id_sales_s == id_sales_valid else id_sales_valid

            del_sales = st.form_submit_button(label="Deletar")
            
            if del_sales:

                sales = id_sales_s.split(' - ')
                id_venda = int(sales[0])
                nome_produto = sales[1]

                df_sales = df_sales[df_sales['id_venda'] != id_venda]
                
                query = f"DELETE FROM sales WHERE id_sales = {id_sales};"
                cur.execute(query)
                conn.commit()

                st.success("Venda deletada com sucesso!")

        st.subheader("Tabela Vendas")
        
        st.write(df_sales)

        save_sales_bt = st.button('Baixar Tabela')
        if save_sales_bt:
            save_table('tabela_vendas', df_sales)
            st.success("Tabela salva com sucesso!")

    if selected == 'Funcionário':
        st.subheader("Registrar Funcionário")
        with st.form(key="reg_employee", clear_on_submit=True):

            id_func_atual = df_employees['id_funcionario'].max()
            if pd.isna(id_func_atual) == False:
                id_func = int(id_func_atual) + 1
            else:
                id_func = 1
            
            nome_func = st.text_input("Nome Funcionário", key='nome_func')
            cpf = st.text_input("CPF", key='cpf')
            data_adesao = st.date_input("Data de Adesão", key='data_adesao', format= "DD/MM/YYYY")
            salario = st.number_input("Salário", key='salario')
            # taxa_comissao = st.number_input("Comissão (%)", key='taxa_comissao')

            submit_emp = st.form_submit_button(label="Salvar")
                
            if submit_emp:
                df_temp_func = pd.DataFrame([{"id_funcionario": id_func, "nome_funcionario": nome_func, "cpf": cpf, "data_adesao": data_adesao, "salario": salario,  "emp_validation": True}])
                df_employees = pd.concat([df_employees, df_temp_func], ignore_index=True)
                
                query = f"INSERT INTO employees (id_funcionario, nome_funcionario, cpf, data_adesao, salario, emp_validation, company_id) VALUES ({id_func}, '{nome_func}', '{cpf}', '{data_adesao}', {salario}, \
                    true, '{company_id}');"
                cur.execute(query)
                conn.commit()

                st.success("Funcionário registrado com sucesso!")

        st.subheader("Atualizar Funcionário")
        with st.form(key="upd_employee", clear_on_submit=True):

            df_employees_valid = df_employees[df_employees['emp_validation'] == True]
            funcionarios = list(df_employees_valid['id_funcionario'].map(str) + ' - ' + df_employees_valid['nome_funcionario'].map(str))

            id_func_valid = None
            if 'sb_employee_upd' in st.session_state:
                id_func_valid = st.session_state['sb_employee_upd']

            id_func_s = st.selectbox('Funcionário', funcionarios, key='sb_employee_upd')
            salario_novo = st.number_input("Salário", key='salario_novo')

            id_func_s = id_func_s if id_func_s == id_func_valid else id_func_valid

            upd_emp = st.form_submit_button(label="Atualizar")
            
            if upd_emp:

                func = id_func_s.split(' - ')
                id_funcionario = int(func[0])

                df_employees.loc[df_employees['id_funcionario'] == id_funcionario, 'salario'] = salario_novo
                
                query = f"UPDATE employees SET salario = {salario_novo} WHERE id_funcionario = {id_funcionario};"
                cur.execute(query)
                conn.commit()

                st.success("Funcionário atualizado com sucesso!")

        st.subheader("Deletar Funcionário")
        with st.form(key="del_employee", clear_on_submit=True):
            
           
            df_employees_valid = df_employees[df_employees['emp_validation'] == True]
            funcionarios = list(df_employees_valid['id_funcionario'].map(str) + ' - ' + df_employees_valid['nome_funcionario'].map(str))

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

                df_employees.loc[df_employees['id_funcionario'] == id_funcionario, 'emp_validation'] = False
                
                query = f"DELETE FROM employees WHERE id_funcionario = {id_funcionario};"
                cur.execute(query)
                conn.commit()

                st.success("Funcionário deletado com sucesso!")

        st.subheader("Tabela Funcionários")
        st.write(df_employees[df_employees['emp_validation'] == True].loc[:, df_employees.columns != 'emp_validation'])

        save_employees_bt = st.button('Baixar Tabela')
        if save_employees_bt:
            save_table('tabela_funcionarios', df_employees[df_employees['emp_validation'] == True].loc[:, df_employees.columns != 'emp_validation'])
            st.success("Tabela salva com sucesso!")

    if selected == 'Produto':
        st.subheader("Registrar Produto")
        with st.form(key="reg_product", clear_on_submit=True):
            
            id_produto_atual = df_products['id_produto'].max()
            if pd.isna(id_produto_atual) == False:
                id_produto = int(id_produto_atual) + 1
            else:
                id_produto = 1

            nome_produto = st.text_input("Nome Produto")
            venda_produto = st.number_input("Valor de Venda")

            submit_prod = st.form_submit_button(label="Salvar")

            if submit_prod:
                df_products = pd.concat([df_products, pd.DataFrame([{"id_produto": id_produto, "nome_produto": nome_produto, 'valor_venda': venda_produto}])], ignore_index=True)
                
                query = f"INSERT INTO products (id_produto, nome_produto, valor_venda, company_id) VALUES ({id_produto}, '{nome_produto}', {venda_produto}, '{company_id}');"
                cur.execute(query)
                conn.commit()

                st.success("Produto registrado com sucesso!")
        
        st.subheader("Atualizar Produto")
        with st.form(key="upd_product", clear_on_submit=True):

            produtos = list(df_products['id_produto'].map(str) + ' - ' + df_products['nome_produto'].map(str))

            id_prod_valid = None
            if 'sb_product_upd' in st.session_state:
                id_prod_valid = st.session_state['sb_product_upd']

            id_prod_s = st.selectbox('Produto', produtos, key='sb_product_upd')
            valor_venda_novo = st.number_input("Valor de Venda", key='valor_venda_novo')

            id_prod_s = id_prod_s if id_prod_s == id_prod_valid else id_prod_valid

            upd_prod = st.form_submit_button(label="Atualizar")
            
            if upd_prod:

                prod = id_prod_s.split(' - ')
                id_produto = int(prod[0])
                nome_produto = prod[1]

                df_products.loc[df_products['id_produto'] == id_produto, 'valor_venda'] = valor_venda_novo
                
                query = f"UPDATE products SET valor_venda = {valor_venda_novo} WHERE id_produto = {id_produto};"
                cur.execute(query)
                conn.commit()

                st.success("Produto deletado com sucesso!")

        st.subheader("Deletar Produto")
        with st.form(key="del_product", clear_on_submit=True):
            
            produtos = list(df_products['id_produto'].map(str) + ' - ' + df_products['nome_produto'].map(str))

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

                df_products = df_products[df_products['id_produto'] != id_produto]
                
                query = f"DELETE FROM products WHERE id_produto = {id_produto};"
                cur.execute(query)
                conn.commit()

                st.success("Produto deletado com sucesso!")

        st.subheader("Tabela Produtos")
        st.write(df_products)

        save_products_bt = st.button('Baixar Tabela')
        if save_products_bt:
            save_table('tabela_produtos', df_products)
            st.success("Tabela salva com sucesso!")

    if selected == 'Despesa':
        st.subheader("Registrar Despesa")
        with st.form(key="despesas", clear_on_submit=True):

            id_desp_atual = df_despesa['id_despesa'].max()
            if pd.isna(id_desp_atual) == False:
                id_desp = int(id_desp_atual) + 1
            else:
                id_desp = 1

            tipo_despesa = st.selectbox('Tipo de Despesa', ['Salário','Material','Conserto'])
            qtd = st.text_input('Quantidade')
            descricao = st.text_input('Descrição')
            valor_despesa = st.number_input('Valor da Despesa')
            valor_despesa = float(valor_despesa)
            data_despesa = st.date_input('Data da Despesa', format= "DD/MM/YYYY")
            submit_desp = st.form_submit_button(label="Salvar")

            if submit_desp:
                qtd = int(qtd)
                data_despesa_abv = f'{data_despesa.year}/{data_despesa.month}'
                df_temp_desp = pd.DataFrame([{'id_despesa': id_desp, 'tipo_despesa': tipo_despesa, 'qtd': qtd, 'descricao': descricao, 'valor_despesa': valor_despesa, 'data_despesa': data_despesa, 
                                              'data_despesa_abv': data_despesa_abv}])
                df_despesa = pd.concat([df_despesa, df_temp_desp], ignore_index=True)
                
                query = f"INSERT INTO despesa (id_despesa, tipo_despesa, qtd, descricao, valor_despesa, data_despesa, data_despesa_abv, company_id) VALUES ({id_desp}, '{tipo_despesa}', {qtd}, '{descricao}', {valor_despesa}, \
                    '{data_despesa}', '{data_despesa_abv}', '{company_id}');"
                cur.execute(query)
                conn.commit()

                st.success("Despesa registrada com sucesso!")

        st.subheader("Deletar Despesa")
        with st.form(key="del_desp", clear_on_submit=True):
            
            despesas = list(df_despesa['id_despesa'].map(str) + ' - ' + df_despesa['tipo_despesa'].map(str))

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

                df_despesa = df_despesa[df_despesa['id_despesa'] != id_desp]
                
                query = f"DELETE FROM despesa WHERE id_despesa = {id_desp};"
                cur.execute(query)
                conn.commit()

                st.success("Despesa deletada com sucesso!")

        st.subheader("Tabela Despesas")
        st.write(df_despesa)

        save_despesa_bt = st.button('Baixar Tabela')
        if save_despesa_bt:
            save_table('tabela_despesa', df_despesa)
            st.success("Tabela salva com sucesso!")
        
    return df_employees, df_products, df_sales, df_despesa
