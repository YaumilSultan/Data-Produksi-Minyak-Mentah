from altair.vegalite.v4.api import Chart
from altair.vegalite.v4.schema.channels import Color
import streamlit as st
import json
import pandas as pd
import altair as alt
from PIL import Image
from streamlit.elements import number_input

st.title('Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia')
image = Image.open('Iroha.png')
st.sidebar.image(image)
st.sidebar.title('いらっしゃいませ (Welcome)')
st.sidebar.subheader('''Creator: M. Yaumil Sultan R.
    NIM: 12219011''')

#nomor 1 -------------------------------------------------------------------------------------------------------------------------

f = open('kode_negara_lengkap.json')
fjson = json.load(f)

df = pd.read_csv('Produksi_minyak_mentah.csv')

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

#nomor 4 ------------------------------------------------------------------------------------------------------------------------------

st.subheader('Jumlah Produksi Terbesar & Terkecil Keseluruhan Tahun')

colum1, colum2 = st.columns(2)

with colum1:
    st.write('Jumlah Produksi Terbesar Keseluruhan Tahun')

    st.caption("Negara: {}  \nProduksi: {}".format(
            df_kumulatif.iloc[0]['Negara'], df_kumulatif.iloc[0]['Kumulatif']))

with colum2:
    st.write('Jumlah Produksi Terkecil Keseluruhan Tahun')

    reversed_df_kumulatif = df_kumulatif.iloc[::-1]

    lowest = []
    low = []
    for i in reversed_df_kumulatif['Kumulatif']:
        for j in reversed_df_kumulatif['Negara']:
            if i != 0:
                lowest.append(i)
                low.append(j)

    reversed_df_kumulatif = pd.DataFrame(list(zip(low, lowest)), columns =['Negara', 'Kumulatif'])

    st.caption("Negara: {}  \nProduksi: {}".format(
            reversed_df_kumulatif.iloc[0]['Negara'], reversed_df_kumulatif.iloc[0]['Kumulatif']))


st.subheader('Jumlah Produksi Terbesar & Terkecil Pada Tahun Tertentu')

df.sort_values(by=['tahun'], ascending=True)
df_max = df.drop_duplicates('tahun')

option2 = st.selectbox(
     'Tahun:',
     (df_max['tahun']))

colum3, colum4 = st.columns(2)

with colum3:
    st.write('Jumlah Produksi Terbesar')

    grouped = df.groupby(df['tahun'])
    df_max = grouped.get_group(option2).sort_values(by=['produksi'], ascending=False)
    df_max = df_max.head(1)

    st.dataframe(df_max)

with colum4:
    st.write('Jumlah Produksi Terkecil')

    grouped = df.groupby(df['tahun'])
    df_max = grouped.get_group(option2).sort_values(by=['produksi'], ascending=True)
    df_max = df_max.loc[(df_max!=0).any(axis=1)]
    df_max = df_max.head(1)

    st.dataframe(df_max)
