from flask import Flask, render_template, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_sensor_data():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT id, value, timestamp FROM sensor_data ORDER BY id DESC LIMIT 20;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows[::-1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    rows = get_sensor_data()
    return jsonify([
        {'id': row[0], 'value': row[1], 'timestamp': row[2].strftime('%H:%M:%S')}
        for row in rows
    ])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')