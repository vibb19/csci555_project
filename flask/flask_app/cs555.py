from flask import Flask, render_template, request, redirect, url_for
import db
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = db.get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    image_path = '"' + posts[0]['image'] + '"'
    print(image_path)
    return posts[0]['title'] + '<br><img src=' + image_path + '>'

@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = db.get_db_connection()
    cursor = conn.cursor()
    posts = cursor.execute("SELECT * FROM items").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)