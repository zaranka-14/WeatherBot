import pandas as pd


available_day = ['1', '2', '3', '4', '5']
available_day_callback = ['day_1', 'day_2', 'day_3', 'day_4', 'day_5']

df = pd.read_csv("data/weather_forecast_train.csv")
df_dict = df.to_dict()


def get_info(x: int, y: int, day: int) -> dict:
    return df_dict[x + y * 30 + day * 900]
