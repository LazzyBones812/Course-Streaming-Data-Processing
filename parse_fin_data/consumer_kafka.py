from confluent_kafka import Producer, Consumer
import re
import pandas as pd
import streamlit as st
import plotly.express as px
import time

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def process_words(message: str) -> list[str]:
    tokens = word_tokenize(message)
    lemmatizer = WordNetLemmatizer()
    tok = []
    for word in tokens:
        t = re.findall(r'\b\w+\b', word.lower())
        if len(t) > 0: 
            tok.append(t[0])
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tok if word not in stopwords.words('english')]
    return filtered_tokens


def count_unique_words(list_w: list) -> pd.DataFrame:
    dict_df = {}
    count = 0
    df_set = set(list_w)
    for i in df_set:
        for j in list_w:
            if i == j:
                count += 1
        dict_df[i] = count
        count = 0
    return pd.DataFrame(list(dict_df.items()), columns=['words', 'count']).sort_values(by='count', ascending=False).reset_index(drop=True)

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "group1",
    "auto.offset.reset": "earliest"
})
consumer.subscribe(['some_topic'])
list_message = []


for _ in range(60):
    msg = consumer.consume(num_messages=1, timeout=2.0)
    if len(msg) > 0:
        list_message.append(msg[0].value().decode())

consumer.close()

list_message = ' '.join(list_message)
df = count_unique_words(process_words(list_message))


producer = Producer({"bootstrap.servers": "localhost:9092"})
for i in range(df.shape[0]):
    producer.produce('res_topic', key=str(df.values[i][0]), value=str(df.values[i][1]))
    producer.flush()
