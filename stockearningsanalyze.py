import pandas as pd
import os
import streamlit as st
import sqlalchemy as db
from dotenv import load_dotenv
import plotly.express as px


def get_db_url():
    load_dotenv()
    PG_USERNAME = os.getenv('PG_USERNAME')
    PG_PASSWORD = os.getenv('PG_PASSWORD')

    PG_URL = db.URL.create(
        'postgresql+psycopg2',
        database='appdb',
        username=PG_USERNAME,
        password=PG_PASSWORD,
        host='127.0.0.1',
        port=5432
    )
    return PG_URL


def load_data(PG_URL):
    sql = "SELECT stock_fiscale_date, stock_reported_eps, stock_symbol FROM stock_generic_info_data"
    engine = db.create_engine(PG_URL, echo=True)
    data = pd.read_sql_query(sql, engine)
    data.dropna(subset=['stock_reported_eps', 'stock_fiscale_date'], inplace=True)
    data.rename(columns={'stock_reported_eps': 'Earning Per Stock'}, inplace=True)
    data.rename(columns={'stock_fiscale_date': 'Fiscal Date'}, inplace=True)
    return data


stock_symbols = ['SYM1', 'SYM2','SYM3']

def main(PG_URL):
    st.header("Earnings Per Stock Raw Data")
    raw_data = load_data(PG_URL)
    if st.checkbox("Show Raw Data", False):
        st.write(raw_data)
    select = st.selectbox('Stock Symbols', stock_symbols)
    for s in stock_symbols:
        if select == s:
            st.header("{0}".format(s) + " Earnings Per Stock Within The Last 12 Months")
            filtered_data = raw_data.query("stock_symbol ==\'{0}\'".format(select))[
                                ['stock_symbol', 'Fiscal Date', 'Earning Per Stock']].sort_values(
                by=['Fiscal Date'], ascending=False).dropna(how='any')[:12]
            st.write(filtered_data)
            fig = px.bar(filtered_data, x='Fiscal Date', y='Earning Per Stock',
                         hover_data=['Fiscal Date', 'Earning Per Stock'], height=400)
            st.write(fig)


if __name__ == "__main__":
    main(get_db_url())
