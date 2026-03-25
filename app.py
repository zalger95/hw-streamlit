import streamlit as st
import plotly.express as px
from analysis import *
from api_weather import get_weather
import datetime

st.title("Анализ температур")
file = st.file_uploader("Загрузите CSV", type=["csv"])

if file:
    df = load_data(file)

    cities = df["city"].unique()
    city = st.selectbox("Выберите город", cities)

    df = df[df["city"] == city]

    df = add_rolling(df)
    stats = stats_season(df)
    df = find_anomalies(df, stats)
    fig = px.line(df, x="timestamp", y="temperature", title="Температура")

    anomalies = df[df["is_anomaly"]]
    fig.add_scatter(x=anomalies["timestamp"], y=anomalies["temperature"],
                    mode='markers', name='Аномалии')

    st.plotly_chart(fig)
    st.write("Статистика:")
    st.dataframe(stats)
    api = st.text_input("Введите API")
    if api:
        temp = get_weather(city, api)
        if isinstance(temp, dict):
            st.error(temp["error"])
        else:
            st.write(f"Текущая температура: {temp}")
            month = datetime.datetime.now().month

            if month in [1, 2, 12]:
                season = "winter"
            elif month in [3, 4, 5]:
                season = "spring"
            elif month in [6, 7, 8]:
                season = "summer"
            else:
                season = "autumn"

            result = check_temperature(temp, stats, city, season)
            st.write(f"Статус: {result}")