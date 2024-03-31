import pandas as pd

available_day = ['1', '2', '3', '4', '5']
available_day_callback = ['day_1', 'day_2', 'day_3', 'day_4', 'day_5']

df = pd.read_csv("data/forecast_data.csv")
df_dict = df.to_dict()


async def get_info(x: int, y: int, hour: int) -> dict:
    return df[(df['longitude'] == x) & (df['latitude'] == y) & (df['hour'] == hour+43)]
