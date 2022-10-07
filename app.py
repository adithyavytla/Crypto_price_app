# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:25:45 2022

@author: adith
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import requests
from PIL import Image

im=Image.open('cryptocurrencies.png')
# Page layout
## Page expands to full width
st.set_page_config(layout="wide",page_title="Crypto App",page_icon=im)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
html_temp = """
<div style="background:#ed0af1 ;padding:10px">
<h2 style="color:white;text-align:center;"> Crypto Price App </h2>
</div>
"""
st.markdown(
 """
<style>
span[data-baseweb="tag"] {
  background-color: #ed0af1 !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(html_temp, unsafe_allow_html = True)
st.markdown("""
            
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **Coingecko API**!

""")
# Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))
col1.header('Input Options')
#data retrieval from coingecko api
@st.cache
def load_data():
    r=requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc')
    df=pd.DataFrame(r.json())
    df.drop('image',inplace=True,axis=1)
    df.index+=1
    return df
#function to round the price change
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a
#call load_data() function
df=load_data()
bdf=pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
col1_selection = st.sidebar.selectbox('Price 1', bdf.symbol, list(bdf.symbol).index('BTCBUSD') )
col2_selection = st.sidebar.selectbox('Price 2', bdf.symbol, list(bdf.symbol).index('ETHBUSD') )


sorted_coin = sorted( df['symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
#filter requested cryptocoins data
df_selected_coin = df[ (df['symbol'].isin(selected_coin)) ]

# Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['24h','Market cap'])
percent_dict = {"24h":'price_change_percentage_24h',"Market cap":'market_cap_change_percentage_24h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])
col1.markdown(''' 
               
''')
col1_df = bdf[bdf.symbol == col1_selection]
col2_df = bdf[bdf.symbol == col2_selection]
col1_price = round_value(col1_df.weightedAvgPrice)
col2_price = round_value(col2_df.weightedAvgPrice)
col1_percent = f'{float(col1_df.priceChangePercent)}%'
col2_percent = f'{float(col2_df.priceChangePercent)}%'
col2.subheader('Selected Cryptos')
col2.metric(col1_selection, col1_price, col1_percent)
col2.metric(col2_selection, col2_price, col2_percent)
col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
col2.dataframe(df_coins)
#code to download the table into csv
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_new = pd.concat([df_coins.symbol,df_coins.current_price,df_coins.price_change_percentage_24h,df_coins.market_cap_change_percentage_24h],axis=1)
df_new=df_new.set_index('symbol')
df_new['new_price_change_percentage_24h'] = df_new['price_change_percentage_24h'] > 0
df_new['new_market_cap_change_percentage_24h'] = df_new['market_cap_change_percentage_24h'] > 0
col2.dataframe(df_new)

col2.markdown(filedownload(df_new), unsafe_allow_html=True)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '24h' and len(selected_coin)>0:
    if sort_values == 'Yes':
        df_new = df_new.sort_values(by=['price_change_percentage_24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_new['price_change_percentage_24h'].plot(kind='barh', color=df_new.new_price_change_percentage_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == 'Market cap' and len(selected_coin)>0:
    if sort_values == 'Yes':
        df_new = df_new.sort_values(by=['market_cap_change_percentage_24h'])
    col3.write('*market cap 24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_new['market_cap_change_percentage_24h'].plot(kind='barh', color=df_new.new_market_cap_change_percentage_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
