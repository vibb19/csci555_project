from flask import Flask, abort, logging, render_template, url_for
from logging.config import dictConfig
import sqlite3, redis, json, time

app = Flask(__name__)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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
    return [dict(id=row['id'], name=row['name'], profilepic=row['profilepic'], img1=row['image1'], img2=row['image2'], img3=row['image3']) for row in users]

def fetch_user_from_db(id):
    """Simulate a slow database query."""
    time.sleep(1)  # optional: simulate latency
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user = dict(id=row['id'], name=row['name'], profilepic=row['profilepic'], img1=row['image1'], img2=row['image2'], img3=row['image3'])
        app.logger.info("id " + str(id) + " found record: " + str(user))
        return user
    else:
        app.logger.info("id " + str(id) + " not found")
        return None

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
    lines += [f"{u['id']}: {u['name']}, {u['profilepic']}, {u['img1']}, {u['img2']}, {u['img3']}" for u in users]
    return "<br>".join(lines)
    
@app.route('/user/<int:id>')
def get_user(id):
    # 1. Try reading from cache
    cached = cache.get(id)
    if cached:
        app.logger.info("Cache HIT for id " + str(id))
        user = json.loads(cached)
        source = "🔵 Served from Cache"
    else:
        app.logger.info("Cache MISS for id " + str(id))
        user = fetch_user_from_db(id)
        # Store JSON-encoded result in Redis with TTL
        cache.set(id, json.dumps(user), ex=CACHE_TTL)
        source = "🟢 Served from Database"
    
    if user:
        # Build a simple HTML response
        lines = [f"{source}"]
        lines += [f"{user['id']}: {user['name']}, {user['profilepic']}, {user['img1']}, {user['img2']}, {user['img3']}"]
        profile_image = url_for('static', filename=f"images/{user['profilepic']}")
        user_image1 = url_for('static', filename=f"images/{user['img1']}")
        user_image2 = url_for('static', filename=f"images/{user['img2']}")
        user_image3 = url_for('static', filename=f"images/{user['img3']}")
        print(profile_image)
        return render_template("index.html", username=user['name'], profile_image=profile_image, user_image1=user_image1, user_image2=user_image2, user_image3=user_image3)
    else:
        return "user not found", 404

@app.route('/clear-cache')
def clear_cache():
    cache.delete(CACHE_KEY)
    return "Cache cleared!"

@app.route('/clear-cache/<int:id>')
def clear_user_cache(id):
    cache.delete(id)
    return f"Cache {id} cleared!"

if __name__ == '__main__':
    app.run(debug=True)
