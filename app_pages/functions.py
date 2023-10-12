import pandas as pd
import numpy as np
import streamlit as st
from core.db import Db_pg

def convert_number(value) -> str:
    '''Convert format number to brazilian type'''

    if pd.isna(value):

        return np.nan
    
    else:
        value = float(value)
        sep_value = f'{value:_.2f}'
        res = sep_value.replace('.',',').replace('_','.')
    
        return res

def get_columns(table: str, cur) -> list:
    '''Get table columns'''

    cur.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    columns = cur.fetchall()
    table_columns = [x[0] for x in columns]

    return table_columns

@st.cache_data(show_spinner=False)
def load_data(company_id):
    '''Load data from database'''

    cur, conn = Db_pg.connect()

    cur.execute(f"SELECT * FROM sales WHERE company_id = '{company_id}';")
    sales_list = list(cur.fetchall())
    table_sales_columns = [desc[0] for desc in cur.description]
    df_sales = pd.DataFrame(sales_list, columns=table_sales_columns)
    df_sales.drop(columns=['company_id'], inplace=True)
    df_sales['data_venda'] = pd.to_datetime(df_sales['data_venda'], format='%Y-%m-%d')
    df_sales['valor_venda'] = df_sales['valor_venda'].astype(float)

    cur.execute(f"SELECT * FROM employees WHERE company_id = '{company_id}';")
    employees_list = list(cur.fetchall())
    table_employees_columns = [desc[0] for desc in cur.description]
    df_employees = pd.DataFrame(employees_list, columns=table_employees_columns)
    df_employees.drop(columns=['company_id'], inplace=True)

    cur.execute(f"SELECT * FROM despesa WHERE company_id = '{company_id}';")
    despesa_list = list(cur.fetchall())
    table_despesa_columns = [desc[0] for desc in cur.description]
    df_despesa = pd.DataFrame(despesa_list, columns=table_despesa_columns)
    df_despesa.drop(columns=['company_id'], inplace=True)
    df_despesa['valor_despesa'] = df_despesa['valor_despesa'].astype(float)

    cur.execute(f"SELECT * FROM products WHERE company_id = '{company_id}';")
    products_list = list(cur.fetchall())
    table_products_columns = [desc[0] for desc in cur.description]
    df_products = pd.DataFrame(products_list, columns=table_products_columns)
    df_products.drop(columns=['company_id'], inplace=True)

    Db_pg.disconnect(cur, conn)

    return df_sales, df_employees, df_despesa, df_products