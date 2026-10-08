"""Learning-only SQL injection fixture. Never deploy this application."""

import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def open_catalog():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE catalog (id INTEGER PRIMARY KEY, name TEXT, category TEXT)"
    )
    connection.executemany(
        "INSERT INTO catalog VALUES (?, ?, ?)",
        (
            (1, "Paper Moon", "books"),
            (2, "Cloud Atlas Puzzle", "games"),
            (3, "The Imaginary Garden", "books"),
        ),
    )
    connection.commit()
    connection.execute("PRAGMA query_only = ON")
    return connection


@app.get("/")
def index():
    return jsonify(
        warning="Intentionally vulnerable learning-only app. Do not deploy.",
        catalog="/catalog?category=books",
    )


@app.get("/catalog")
def catalog():
    category = request.args.get("category", "")
    connection = open_catalog()
    try:
        if category:
            query = "SELECT id, name, category FROM catalog WHERE category = ? ORDER BY id"
            rows = connection.execute(query, (category,)).fetchall()
        else:
            rows = connection.execute(
                "SELECT id, name, category FROM catalog ORDER BY id"
            ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        connection.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
