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
        cursor.execute(
            "SELECT latitude, longitude FROM events WHERE type not in ('Вызов с молчанием', 'Случайный набор номера', 'Прерывание вызова звонящим сразу после подключения', 'Получение справок', 'Автоматические ложные вызовы', 'Детские шалости', 'не задано','Неправильный набор номера (ошибочный)', 'Ложные вызовы вследствие сбоя в сети связи', 'Тренировка','Тест Соседний субъект')")
        data = cursor.fetchall()
        print(data)
        self.connection.close()
        return data

    def select_events_counts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT type, COUNT(DISTINCT id) AS qty FROM events GROUP BY type")
        data = cursor.fetchall()
        cursor.close()
        return data

    def select_by_time(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT
            HOUR(time) AS hour,
            COUNT(*) AS qty
            FROM events
            GROUP BY HOUR(time)
            ORDER BY hour;""")
        times = cursor.fetchall()
        cursor.close()
        return times

    def select_by_month(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT
            MONTH(date) AS month,
            COUNT(*) AS qty
            FROM events
            GROUP BY MONTH(date);""")
        times = cursor.fetchall()
        cursor.close()
        return times

    def select_points(self, lat_1, lon_1, lat_2, lon_2):
        cursor = self.connection.cursor(pymysql.cursors.SSCursor)

        cursor.execute(
            f"""SELECT latitude, longitude
                FROM events
                WHERE (latitude BETWEEN {lat_1} AND {lat_2})
                AND (longitude BETWEEN {lon_1} AND {lon_2})
                AND (type NOT IN ('Вызов с молчанием', 'Случайный набор номера', 'Прерывание вызова звонящим сразу после подключения', 'Получение справок', 'Автоматические ложные вызовы', 'Детские шалости', 'не задано', 'Неправильный набор номера (ошибочный)', 'Ложные вызовы вследствие сбоя в сети связи', 'Тренировка', 'Тест Соседний субъект'))""")
        data = cursor.fetchall()
        self.connection.close()
        return data

    def select_points_by_types(self, lat_1, lon_1, lat_2, lon_2, point_type):
        cursor = self.connection.cursor(pymysql.cursors.SSCursor)
        cursor.execute(
            f"""SELECT latitude, longitude
                FROM events
                WHERE (latitude BETWEEN {lat_1} AND {lat_2})
                AND (longitude BETWEEN {lon_1} AND {lon_2})
                AND (type IN ({"'" + "', '".join(point_type) + "'"}))""")
        data = cursor.fetchall()
        self.connection.close()
        return data

    def select_types(self):
        cursor = self.connection.cursor(pymysql.cursors.SSCursor)
        cursor.execute(
            f"""SELECT type FROM events WHERE type NOT IN ('Вызов с молчанием', 'Случайный набор номера', 'Прерывание вызова звонящим сразу после подключения', 'Получение справок', 'Автоматические ложные вызовы', 'Детские шалости', 'не задано', 'Неправильный набор номера (ошибочный)', 'Ложные вызовы вследствие сбоя в сети связи', 'Тренировка', 'Тест Соседний субъект') GROUP BY type""")
        data = cursor.fetchall()
        self.connection.close()
        return data

    def select_types_qty(self):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT type, count(id) as qty FROM events GROUP BY type""")
        data = cursor.fetchall()
        self.connection.close()
        return data