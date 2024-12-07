import streamlit as st
import confluent_kafka
from confluent_kafka import Consumer, TopicPartition
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time


st.title("Анализ текстов финансовых новостей с YahooFinance по популярным ценным бумагам")
st.write("""Данные собираются с ресурса YahooFinance, полученные данные записываются в kafka, после загружаеются
        из kafka, обрабатываются, считаются количество уникальных слов и строится гистограмма 
        полученных данных""")
st.sidebar.title("About")
st.sidebar.info(""" Приложение по курсу 'Потоковая обработка данных' """)
st.sidebar.info("Репозиторий проекта по курсу "
                "[here](https://github.com/LazzyBones812/Course-Streaming-Data-Processing).")

consumer = Consumer({
    "bootstrap.servers": "kafka:29092",
    "group.id": "group1",
    "auto.offset.reset": "earliest"
})
consumer.subscribe(['res_topic'])


@st.fragment(run_every=60.0)
def recv_data():
    list_key = []
    list_value = []
    global df

    try:
        tp = TopicPartition('res_topic', 0, confluent_kafka.OFFSET_BEGINNING)
        consumer.assign([tp])
        consumer.seek(tp)
        for _ in range(60):
            msg = consumer.consume(num_messages=1, timeout=5.0)
            if len(msg) > 0:
                list_key.append(msg[0].key().decode())
                list_value.append(msg[0].value().decode())
        df = pd.DataFrame({'word' : list_key, 'count' : list_value}).head(15)
        fig = px.bar(df, x='word', y='count', barmode='group')
        st.plotly_chart(fig)
    except confluent_kafka.KafkaException:
        st.write("""Ошибка""")
        fig = px.bar(df, x='word', y='count', barmode='group')
        st.plotly_chart(fig)
    
recv_data()
