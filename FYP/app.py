from flask import Flask, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="attendanceadmin",
        passwd="pimylifeup",
        database="attendancesystem"
    )

@app.route('/attendance/last_2_hours')
def get_recent_attendance():
    two_hours_ago = datetime.now() - timedelta(hours=2)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM attendance WHERE timestamp >= %s"
    cursor.execute(query, (two_hours_ago,))

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)