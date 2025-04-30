<<<<<<< HEAD
from flask import Flask, abort, logging, render_template, url_for, jsonify
=======
from flask import Flask, abort, logging, render_template, url_for, make_response
>>>>>>> 06463dd4c8d121a7374747b603ba212068261872
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

# -------------
# Configuration
# -------------
DATABASE = 'mydatabase.db'
CACHE_KEY = 'all_users'
CACHE_TTL = 100  # cache TTL in seconds
NUM_RECORDS = 20000

# Connect to Redis (make sure redis-server is running)
cache = redis.Redis(host='localhost', port=6379, db=0)

# -------------
# Helpers
# -------------
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

# -------------
# Routes
# -------------
@app.route('/')
def index():
    cached = cache.get(CACHE_KEY)
    if cached:
        app.logger.info("Cache HIT")
        users = json.loads(cached)
        source = "🔵 Served from Cache"
    else:
        app.logger.info("Cache MISS")
        all_users = fetch_users_from_db()  # Full 20k records from DB
        
        # Try caching progressively smaller batches
        users = all_users  # Default to full dataset
        for batch_size in range(NUM_RECORDS, 0, -500):
            try:
                serialized = json.dumps(all_users[:batch_size])
                cache.set(CACHE_KEY, serialized)
                users = all_users[:batch_size]  # Use cached subset
                source = f"🟢 Served from DB (cached {batch_size} records)"
                break
            except redis.exceptions.OutOfMemoryError:
                app.logger.warning(f"OOM at {batch_size} records, retrying...")
                continue
        else:
            # If all batches fail, serve uncached
            users = all_users
            source = "🟡 Served from DB (no caching possible)"
            app.logger.error("All cache attempts failed - Redis OOM")

    # Build response
    lines = [f"{source}"]
    lines += [f"{u['id']}: {u['name']}" for u in users]
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
        if user:  # Only cache if user exists
            cache.set(id, json.dumps(user), ex=CACHE_TTL)
        source = "🟢 Served from Database"
    
    if user:
        # Build a simple HTML response
        profile_image = url_for('static', filename=f"images/{user['profilepic']}")
        user_image1 = url_for('static', filename=f"images/{user['img1']}")
        user_image2 = url_for('static', filename=f"images/{user['img2']}")
        user_image3 = url_for('static', filename=f"images/{user['img3']}")
<<<<<<< HEAD
        return render_template("index.html", 
                            username=user['name'], 
                            profile_image=profile_image, 
                            user_image1=user_image1,
                            user_image2=user_image2,
                            user_image3=user_image3)
=======
        
        #print(profile_image)
        response = make_response(render_template("index.html", username=user['name'], profile_image=profile_image, user_image1=user_image1, user_image2=user_image2, user_image3=user_image3))
        if cached:
            response.headers['X-App-Cache-Status'] = 'HIT'
        else:
            response.headers['X-App-Cache-Status'] = 'MISS'
        return response
>>>>>>> 06463dd4c8d121a7374747b603ba212068261872
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

# New metrics endpoint
@app.route('/metrics')
def redis_metrics():
    try:
        # Get Redis statistics
        stats = cache.info('stats')
        memory = cache.info('memory')
        
        # Calculate cache hit ratio
        hits = int(stats['keyspace_hits'])
        misses = int(stats['keyspace_misses'])
        hit_ratio = hits / (hits + misses) if (hits + misses) > 0 else 0
        
        return jsonify({
            'hits': hits,
            'misses': misses,
            'hit_ratio': round(hit_ratio, 4),
            'hit_ratio_percent': round(hit_ratio * 100, 2),
            'evicted_keys': stats.get('evicted_keys', 0),
            'total_keys': cache.dbsize(),
            'memory_used': memory['used_memory'],
            'memory_used_human': memory['used_memory_human'],
            'maxmemory': memory.get('maxmemory', 0),
            'maxmemory_human': f"{memory.get('maxmemory', 0) // 1024 // 1024}MB" if memory.get('maxmemory') else 'unlimited'
        })
    except redis.RedisError as e:
        app.logger.error(f"Redis error: {str(e)}")
        return jsonify({'error': 'Redis unavailable'}), 500

if __name__ == '__main__':
    app.run(debug=True)
