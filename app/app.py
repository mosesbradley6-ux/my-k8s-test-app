from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"]
    )

@app.route("/")
def home():
    return "Task Tracker Running"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks;")
    rows = cur.fetchall()
    conn.close()

    return jsonify([{"id": r[0], "title": r[1], "done": r[2]} for r in rows])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id;",
        (data["title"], False)
    )

    task_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"id": task_id, "title": data["title"], "done": False})
