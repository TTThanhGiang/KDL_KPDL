from flask import Flask, request, jsonify
from flask_cors import CORS
import pytz
from datetime import datetime

import mysql.connector

app = Flask(__name__)
CORS(app)

# Kết nối đến MySQL
db_connection = mysql.connector.connect(
    host="database",  # Tên dịch vụ trong docker-compose
    user="root",
    password="password",
    database="crypto_db"
)
cursor = db_connection.cursor()

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.json
    try:
        cursor.execute(
            """
            INSERT INTO coin_data (symbol, price, volume, highPrice, lowPrice, time) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['symbol'], data['price'], data['volume'], data['highPrice'], data['lowPrice'], data['time'])
        )
        db_connection.commit()
        return jsonify({"message": "Data inserted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthcheck', methods=['GET'])
def health_check():
    try:
        cursor.execute("SELECT 1")
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        cursor.execute("SELECT * FROM coin_data")  # Truy vấn lấy dữ liệu từ bảng
        rows = cursor.fetchall()
        # Định dạng kết quả thành JSON
        data = []
        for row in rows:
            data.append({
                'id': row[0],
                'symbol': row[1],
                'price': row[2],
                'volume': row[3],
                'highPrice': row[4],
                'lowPrice': row[5],
                'time': row[6].astimezone(vietnam_timezone).strftime('%Y-%m-%d %H:%M:%S')  # Chuyển đổi thời gian về múi giờ Việt Nam
            })
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
