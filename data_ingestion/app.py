import requests
import time
from datetime import datetime
import logging
import pandas as pd
from binance.client import Client
import mysql.connector

# Thiết lập logging
logging.basicConfig(level=logging.INFO)

# Kết nối đến MySQL
db_connection = mysql.connector.connect(
    host="database",  # Tên dịch vụ MySQL trong Docker Compose
    user="root",
    password="password",
    database="crypto_db"
)
cursor = db_connection.cursor()

API_KEY = 'QazS8hMu4kK0SUGIuAJYD1RRJYRHA3wAeBwfRCcLUP3Yc9maH8DmBGloCQ46ohHm'
API_SECRET = 'mcK4w9YckLLavlDpnsxvjyYXqaF14ZznFss4UIKlszKpcxSvf9ufKY3kfZ3VdkpE'

# Khởi tạo client Binance
client = Client(api_key=API_KEY, api_secret=API_SECRET)

# Hàm lấy dữ liệu thô từ API
def get_raw_data(symbol):
    try:
        ticker_info = client.get_ticker(symbol=symbol)
        return ticker_info
    except Exception as e:
        logging.error(f"Error getting raw data for {symbol}: {str(e)}")
        return None

# Hàm chuẩn bị dữ liệu
def prepare_data(raw_data):
    try:
        # Chuẩn bị dữ liệu
        data = {
            'symbol': raw_data['symbol'],
            'price': float(raw_data['lastPrice']),
            'volume': float(raw_data['volume']),
            'highPrice': float(raw_data['highPrice']),
            'lowPrice': float(raw_data['lowPrice']),
            'time': pd.to_datetime('now').isoformat()
        }
        return data
    except Exception as e:
        logging.error(f"Error preparing data: {str(e)}")
        return None



# Hàm chèn dữ liệu vào cơ sở dữ liệu
def insert_to_db(data):
    url = "http://database_api:5000/insert"  # Sử dụng tên dịch vụ trong Docker Compose
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            logging.info("Data inserted successfully.")
        else:
            logging.error(f"Failed to insert data: {response.json()}")
    except Exception as e:
        logging.error(f"Error inserting data: {str(e)}")

# Hàm chính để thu thập dữ liệu
def main():
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    while True:
        start_time = time.time()
        for symbol in symbols:
            raw_data = get_raw_data(symbol)
            if raw_data:
                data = prepare_data(raw_data)           
                if data:
                    insert_to_db(data)

        end_time = time.time()
        logging.info(f"Data collection took {end_time - start_time} seconds.")
        time.sleep(30)  # Thời gian giữa các lần gọi API

if __name__ == "__main__":
    main()
