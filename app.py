from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock, Semaphore
from datetime import datetime
import sqlite3
from recommender import recommend_careers
from scheduler import fcfs, sjf, round_robin

app = Flask(__name__)
DB = "careerpath.db"
executor = ThreadPoolExecutor(max_workers=4)
request_queue = Queue()
db_lock = Lock()
recommendation_slots = Semaphore(4)

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                domain TEXT NOT NULL,
                skills TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def process_profile(payload):
    # Semaphore limits the number of recommendation jobs using this shared service.
    with recommendation_slots:
        results = recommend_careers(payload["interests"], payload["skills"], payload["education"])
        top = results[0]["career"] if results else "Explore foundational skills"
        with db_lock:
            with sqlite3.connect(DB) as con:
                con.execute(
                    "INSERT INTO requests(name, domain, skills, recommendation, created_at) VALUES (?, ?, ?, ?, ?)",
                    (payload["name"], payload["education"], ", ".join(payload["skills"]), top,
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
        request_queue.put({"name": payload["name"], "top": top})
        return results

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    payload = {
        "name": request.form.get("name", "").strip() or "Student",
        "education": request.form.get("education", "Undergraduate"),
        "interests": request.form.get("interests", "").lower(),
        "skills": [s.strip().lower() for s in request.form.get("skills", "").split(",") if s.strip()]
    }
    future = executor.submit(process_profile, payload)
    results = future.result()
    return render_template("index.html", results=results, submitted_name=payload["name"])

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json(silent=True) or {}
    payload = {
        "name": str(data.get("name", "API Student")),
        "education": str(data.get("education", "Undergraduate")),
        "interests": str(data.get("interests", "")).lower(),
        "skills": [str(s).lower() for s in data.get("skills", [])]
    }
    future = executor.submit(process_profile, payload)
    return jsonify({"recommendations": future.result()})

@app.route("/api/history")
def history():
    with db_lock:
        with sqlite3.connect(DB) as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM requests ORDER BY id DESC LIMIT 10").fetchall()
    return jsonify([dict(row) for row in rows])

@app.route("/api/health")
def health():
    return jsonify({"status": "running", "worker_threads": 4, "queued_events": request_queue.qsize()})

@app.route("/scheduler")
def scheduler_demo():
    jobs = [{"pid": "P1", "arrival": 0, "burst": 5},
            {"pid": "P2", "arrival": 1, "burst": 3},
            {"pid": "P3", "arrival": 2, "burst": 1}]
    return jsonify({
        "FCFS": fcfs(jobs),
        "SJF": sjf(jobs),
        "Round Robin (quantum=2)": round_robin(jobs, 2)
    })

if __name__ == "__main__":
    init_db()
    print("CareerPath OS running at http://127.0.0.1:5000")
    app.run(debug=True, threaded=True)
