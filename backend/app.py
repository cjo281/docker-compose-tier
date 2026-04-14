from flask import Flask, jsonify
import psycopg2
import redis
import os

# Create the Flask application
app = Flask(__name__)

# -----------------------------
# PostgreSQL CONNECTION FUNCTION
# -----------------------------
# This function creates a new connection to the PostgreSQL database
# using environment variables passed from docker-compose.yml.
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),       # database service name
        database=os.getenv("POSTGRES_DB"),     # database name
        user=os.getenv("POSTGRES_USER"),       # username
        password=os.getenv("POSTGRES_PASSWORD")# password
    )

# -----------------------------
# REDIS CONNECTION
# -----------------------------
# Redis client used for caching tests.
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),  # redis service name
    port=6379,                     # default redis port
    decode_responses=True          # return strings instead of bytes
)

# -----------------------------
# BASIC ROUTE
# -----------------------------
@app.route("/")
def home():
    return jsonify({"message": "Flask API is running!"})

# -----------------------------
# DATABASE TEST ROUTE
# -----------------------------
# This route tests if the API can connect to PostgreSQL.
@app.route("/db")
def db_test():
    try:
        conn = get_db_connection()   # open DB connection
        cur = conn.cursor()
        cur.execute("SELECT NOW();") # simple query
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"db_time": result[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# REDIS TEST ROUTE
# -----------------------------
@app.route("/cache")
def cache_test():
    redis_client.set("test_key", "Hello from Redis!")
    value = redis_client.get("test_key")
    return jsonify({"redis_value": value})

# -----------------------------
# RUN THE APP
# -----------------------------
# host=0.0.0.0 allows the container to expose the API externally.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)