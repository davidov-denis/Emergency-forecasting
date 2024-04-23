import pymysql
from config_db import *


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

    def insert_event_info(self, event_type, lattitude, longitude, card_id):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (NULL, %s, %s, %s, %s)", (event_type, lattitude, longitude, card_id))
        self.connection.commit()

    def select_events_lattitude_longitude(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT latitude, longitude FROM events")
        data = cursor.fetchall()
        points = []
        for row in data:
            points.append([row['latitude'], row['longitude']])
        self.connection.close()
        return points
