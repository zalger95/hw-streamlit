import pandas as pd
from multiprocessing import Pool

def load_data(file):
    df = pd.read_csv(file, parse_dates=["timestamp"])
    return df

def add_rolling(df):
    df = df.sort_values('timestamp')
    df['rolling_mean'] = df.groupby("city")["temperature"].transform(lambda x: x.rolling(window=30).mean())
    return df

def stats_season(df):
    stats = df.groupby(["city", "season"])["temperature"].agg(["mean", "std"]).reset_index()
    return stats

def find_anomalies(df, stats):
    df = df.merge(stats, on=["city", "season"])
    df["is_anomaly"] = ((df["temperature"]>df["mean"]+2*df["std"]) | (df["temperature"]>df["mean"]-2*df["std"]))
    return df

# параллелизация

def process_city(city_df):
    city_df["rolling_mean"] = city_df("temperature").rolling(30).mean()
    return city_df

def parallel(df):
    cities = [group for _, group in df.groupby("city")]
    with Pool() as p:
        result = p.map(process_city, cities)
        return pd.concat(result)


def check_temperature(temp, stats, city, season):
    row = stats[(stats.city == city) & (stats.season == season)]

    mean = row["mean"].values[0]
    std = row["std"].values[0]

    if temp > mean + 2 * std or temp < mean - 2 * std:
        return "Аномалия"
    return "Норма"

