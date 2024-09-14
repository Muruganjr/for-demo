from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='db',  # MySQL hostname; should match the Docker service name
        user='root',
        password='password',
        database='flaskdb'
    )

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add', methods=['POST'])
def add_user():
    name = request.json['name']
    age = request.json['age']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added successfully!'})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
