import csv
import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime

class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params = None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()

def read_csv_file(file_path):
    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 스킵
        for row in reader:
            mars_date_str = row[1]  # '2050.1.1' 또는 '2050-01-01'
            temp = float(row[2])
            storm = int(row[3])  # stom → storm 으로 수정 권장

            # 날짜 변환 - 유연하게 처리
            try:
                mars_date_obj = datetime.strptime(mars_date_str, '%Y.%m.%d')
            except ValueError:
                mars_date_obj = datetime.strptime(mars_date_str, '%Y-%m-%d')

            # 최종 datetime 객체
            mars_date_final = mars_date_obj.strftime('%Y-%m-%d %H:%M:%S')
            mars_date_dt = datetime.strptime(mars_date_final, '%Y-%m-%d %H:%M:%S')

            data_list.append((mars_date_dt, temp, storm))

    return data_list



def insert_data_to_db(helper, data_list):
    insert_query = (
        'INSERT INTO mars_weather (mars_date, temp, storm) '
        'VALUES (%s, %s, %s)'
    )
    for record in data_list:
        helper.execute_query(insert_query, record)

def generate_summary_png(helper):
    query = 'SELECT mars_date, temp, storm FROM mars_weather ORDER BY mars_date ASC'
    result = helper.fetch_all(query)

    dates = [row[0] for row in result]
    temps = [row[1] for row in result]
    storms = [row[2] for row in result]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, temps, label='Temperature (°C)', color='red')
    plt.plot(dates, storms, label='Storm', color='blue')
    plt.title('Mars Weather Summary')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('mars_weather_summary.png')
    plt.close()

def main():
    host = 'localhost'
    user = 'mars_user'
    password = 'mars_passwd1234!'
    database = 'mars_mission'

    helper = MySQLHelper(host, user, password, database)

    csv_file_path = '/Users/cheon-yechan/Desktop/workspace/ia-codyseeay/12week/mars_weathers_data.CSV'
    data_list = read_csv_file(csv_file_path)

    insert_data_to_db(helper, data_list)
    generate_summary_png(helper)

    helper.close()

if __name__ == '__main__':
    main()