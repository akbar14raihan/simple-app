import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_conn():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                dbname=os.getenv("DB_NAME", "appdb"),
                user=os.getenv("DB_USER", "appuser"),
                password=os.getenv("DB_PASS", "apppass"),
            )
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("Database tidak bisa dihubungi")

@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT NOW())")
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"Hello dari simple-app! Halaman ini sudah dikunjungi {total} kali (data dari PostgreSQL)."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
