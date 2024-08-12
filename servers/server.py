from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite Database
def init_sqlite_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result REAL NOT NULL,
            datastream_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()

# Route to receive sensor data
@app.route('/api/endpoint', methods=['POST'])
def receive_sensor_data():
    if request.method == 'POST':
        data = request.json
        result = data['result']
        datastream_id = data['Datastream']['@iot.id']
        
        # Insert into SQLite database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (result, datastream_id)
            VALUES (?, ?)
        ''', (result, datastream_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Data received"}), 201

# Route to view all sensor data
@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor_data')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'result': row[1],
            'datastream_id': row[2],
            'timestamp': row[3]
        })
    
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, ssl_context=('cert.pem', 'key.pem'))