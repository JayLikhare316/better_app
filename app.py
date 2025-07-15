from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from contextlib import contextmanager
import logging

app = Flask(__name__)

# Environment configuration
FLASK_ENV = os.getenv("FLASK_ENV", "production")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Database configuration
if FLASK_ENV == "development":
    DB_PATH = os.getenv("DB_PATH", "./dev_names.db")
    logger.info("Running in development mode")
else:
    DB_PATH = os.getenv("DB_PATH", "/data/names.db")


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database with names table"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS names (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """
        )
        conn.commit()


def get_all_names():
    """Get all names from database"""
    with get_db() as conn:
        cursor = conn.execute("SELECT id, name FROM names ORDER BY id")
        return cursor.fetchall()


def add_name_to_db(name):
    """Add name to database"""
    with get_db() as conn:
        conn.execute("INSERT INTO names (name) VALUES (?)", (name,))
        conn.commit()


def update_name_in_db(name_id, new_name):
    """Update name in database"""
    with get_db() as conn:
        conn.execute("UPDATE names SET name = ? WHERE id = ?", (new_name, name_id))
        conn.commit()


def delete_name_from_db(name_id):
    """Delete name from database"""
    with get_db() as conn:
        conn.execute("DELETE FROM names WHERE id = ?", (name_id,))
        conn.commit()


@app.route("/")
def index():
    names = get_all_names()
    return render_template("index.html", names=names)


@app.route("/add", methods=["POST"])
def add_name():
    name = request.form.get("name")
    if name and name.strip():
        add_name_to_db(name.strip())
    return redirect(url_for("index"))


@app.route("/edit/<int:name_id>", methods=["GET", "POST"])
def edit_name(name_id):
    if request.method == "POST":
        new_name = request.form.get("new_name")
        if new_name and new_name.strip():
            update_name_in_db(name_id, new_name.strip())
        return redirect(url_for("index"))

    with get_db() as conn:
        cursor = conn.execute("SELECT name FROM names WHERE id = ?", (name_id,))
        result = cursor.fetchone()
        if not result:
            return redirect(url_for("index"))

    return render_template("edit.html", name=result[0], name_id=name_id)


@app.route("/delete/<int:name_id>")
def delete_name(name_id):
    delete_name_from_db(name_id)
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    init_db()
    logger.info(f"Starting Better App in {FLASK_ENV} mode")
    app.run(host="0.0.0.0", port=5000, debug=FLASK_DEBUG)
