from flask import Flask
import sqlite3, redis, json, time

app = Flask(__name__)

# —————————————
# Configuration
# —————————————
DATABASE = 'mydatabase.db'
CACHE_KEY = 'all_users'
CACHE_TTL = 15  # cache TTL in seconds

# Connect to Redis (make sure redis-server is running)
cache = redis.Redis(host='localhost', port=6379, db=0)

# —————————————
# Helpers
# —————————————
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_users_from_db():
    """Simulate a slow database query."""
    time.sleep(1)  # optional: simulate latency
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    # Convert to list of dicts for JSON serialization
    return [dict(id=row['id'], name=row['name']) for row in users]

# —————————————
# Routes
# —————————————
@app.route('/')
def index():
    # 1. Try reading from cache
    cached = cache.get(CACHE_KEY)
    if cached:
        app.logger.info("Cache HIT")
        users = json.loads(cached)
        source = "🔵 Served from Cache"
    else:
        app.logger.info("Cache MISS")
        users = fetch_users_from_db()
        # Store JSON-encoded result in Redis with TTL
        cache.set(CACHE_KEY, json.dumps(users), ex=CACHE_TTL)
        source = "🟢 Served from Database"

    # Build a simple HTML response
    lines = [f"{source}"]
    lines += [f"{u['id']}: {u['name']}" for u in users]
    return "<br>".join(lines)

@app.route('/clear-cache')
def clear_cache():
    cache.delete(CACHE_KEY)
    return "Cache cleared!"

if __name__ == '__main__':
    app.run(debug=True)
