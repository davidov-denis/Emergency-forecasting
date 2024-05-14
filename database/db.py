import pymysql
from database.config_db import *


class BaseSQL:
    def __init__(self):
        """Инициализация подключения"""
        self.connection = pymysql.connect(
            host=MYSQLHOST,
            port=MYSQLPORT,
            user=MYSQLUSER,
            password=MYSQLPASSWORD,
            database=MYSQLDATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __exit__(self):
        self.connection.commit()


class EventInfo(BaseSQL):
    def __init__(self):
        super().__init__()

    def insert_event_info(self, event_type, latitude, longitude, card_id, date, time):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                       (event_type, latitude, longitude, card_id, date, time))
        self.connection.commit()

    def insert_event_info_list(self, event_list):
        cursor = self.connection.cursor()
        cursor.executemany("INSERT INTO events VALUES (NULL, %s, %s, %s, %s, %s, %s)", event_list)
        self.connection.commit()

    def select_events_latitude_longitude(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT latitude, longitude FROM events")
        data = cursor.fetchall()
        points = []
        for row in data:
            points.append([row['latitude'], row['longitude']])
        self.connection.close()
        return points

    def select_events_counts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT type, COUNT(DISTINCT id) AS qty FROM events GROUP BY type")
        data = cursor.fetchall()
        cursor.close()
        return data

    def select_by_time(self):
        cursor = self.connection.cursor()
        times = []
        for i in range(0, 24):
            cursor.execute(f"SELECT count(id) AS qty FROM events WHERE time > '{i}:00:00' AND time < '{i + 1}:00:00'")
            data = cursor.fetchall()
            data = data[0]['qty']
            times.append({'start': i, 'end': i + 1, 'qty': data})
        cursor.close()
        return times

    def select_points(self, lat_1, lon_1, lat_2, lon_2):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM events WHERE {lat_1} > latitude and latitude < {lat_2} and {lon_1} > longitude and longitude < {lon_2} and latitude != 0 and longitude != 0")
        data = cursor.fetchall()
        points = []
        for row in data:
            points.append([row['latitude'], row['longitude']])
        self.connection.close()
        return points
