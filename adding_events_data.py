import json
import os

import pandas as pd
from database.db import *
import datetime as dt
import csv

for file in os.listdir("data\\"):
    if ".pkl" in file:
        filename = file[:-4]
    else:
        continue
    print(filename)
    try:
        df = pd.read_pickle(f"data\\{filename}.pkl")
        df = df[['type', 'point', 'cardId', 'timeIsoStr']]
        df.reset_index()
    except BaseException as e:
        print("======", filename, e)
        continue
    count = 0
    with open(f'data/csv/{filename}.csv', 'w', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for index, row in df.iterrows():
            if type(row['point']) == str:
                # обработка дата/время
                datetime = dt.datetime.fromisoformat(row['timeIsoStr'])
                date = datetime.date()
                time = datetime.time()
                # обработка координат
                try:
                    point = json.loads(row['point'])[0]
                except BaseException as e:
                    point = dict(row['point'])
                # обработка значений
                event_type = row['type']
                try:
                    latitude = point['lat']
                    longitude = point['lon']
                except BaseException as e:
                    latitude = 0
                    longitude = 0
                card_id = row['cardId']
                writer.writerow([event_type, latitude, longitude, card_id, date, time])
            count += 1
