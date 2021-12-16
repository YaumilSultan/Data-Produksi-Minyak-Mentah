from altair.vegalite.v4.api import Chart
from altair.vegalite.v4.schema.channels import Color
import streamlit as st
import json
import pandas as pd
import altair as alt
from PIL import Image
from streamlit.elements import number_input

st.title('Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia')
image = Image.open('https://github.com/YaumilSultan/Data-Produksi-Minyak-Mentah/blob/24e360e2609a69bd7f4bcbb744b44488b91f3a8e/Iroha.png')
st.sidebar.image(image)
st.sidebar.title('いらっしゃいませ (Welcome)')
st.sidebar.subheader('''Creator: M. Yaumil Sultan R.
    NIM: 12219011''')

#nomor 1 -------------------------------------------------------------------------------------------------------------------------

f = open('https://github.com/YaumilSultan/Data-Produksi-Minyak-Mentah/blob/24e360e2609a69bd7f4bcbb744b44488b91f3a8e/kode_negara_lengkap.json')
fjson = json.load(f)

df = pd.read_csv('https://github.com/YaumilSultan/Data-Produksi-Minyak-Mentah/blob/24e360e2609a69bd7f4bcbb744b44488b91f3a8e/Produksi_minyak_mentah.csv')

df1=df['kode_negara'].values.tolist()
df2=[]

for i in df1:
    for j in fjson:
        if i == j['alpha-3']:
            i = j['name']
    df2.append(i)

df['kode_negara'] = df2

df.sort_values(by=['kode_negara'], ascending=True)
df_new = df.drop_duplicates('kode_negara')

option = st.selectbox(
     'Pilih Negara:',
     (df_new['kode_negara']))

grouped = df.groupby(df['kode_negara'])
df_new = grouped.get_group(option)
        
chart = alt.Chart(df_new).mark_line().encode(alt.X('tahun'),alt.Y('produksi'))
st.altair_chart(chart, use_container_width=True)

#nomor 2 ------------------------------------------------------------------------------------------------------------------------------

st.subheader('Grafik Jumlah Produksi Terbesar pada Tahun Tertentu')

df.sort_values(by=['tahun'], ascending=True)
df_new = df.drop_duplicates('tahun')

option1 = st.selectbox(
     'Pilih Tahun:',
     (df_new['tahun']))

grouped = df.groupby(df['tahun'])
df_new = grouped.get_group(option1).sort_values(by=['produksi'], ascending=False)


number = int(st.number_input('Jumlah Negara',min_value=1, max_value=196))
dfnew=df_new.head(number)

bar1 = alt.Chart(dfnew).mark_bar().encode(alt.X('kode_negara'),alt.Y('produksi'))
st.altair_chart(bar1, use_container_width=True)

#nomor 3 ------------------------------------------------------------------------------------------------------------------------------

st.subheader('Grafik Jumlah Produksi Terbesar secara Kumulatif')

number1 = int(st.number_input('Negara:',min_value=1, max_value=196))

negara = []
for i in df['kode_negara']:
    if i not in negara:
        negara.append(i)

lst = []
for i in negara:
    lst.append(df[df['kode_negara'] == i]['produksi'].sum())

df_kumulatif = pd.DataFrame(list(zip(negara, lst)), columns =['Negara', 'Kumulatif']).sort_values(by=['Kumulatif'], ascending=False)

bar2 = alt.Chart(df_kumulatif.head(number1)).mark_bar().encode(alt.X('Negara'),alt.Y('Kumulatif'))
st.altair_chart(bar2, use_container_width=True)
