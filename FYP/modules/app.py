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
    one_hours_ago = datetime.now() - timedelta(hours=1)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM attendance WHERE clock_in >= %s"
    cursor.execute(query, (one_hours_ago,))

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    # http://192.168.1.10:5000/attendance/last_2_hours
    # insert raspberry pi IP address
