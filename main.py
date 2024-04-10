import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

DATABASE = 'application.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Replace your existing vartotojai and uzrasai routes with the following
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/vartotojai', methods=['GET', 'POST'])
def vartotojai():
    db = get_db()
    if request.method == 'POST':
        vartotojo_vardas = request.form.get('vardas')
        if vartotojo_vardas:
            db.execute('INSERT INTO users (name) VALUES (?)', (vartotojo_vardas,))
            db.commit()
            return redirect(url_for('vartotojai'))
    # Fetch each user and their notes. This requires a more complex query or multiple queries.
    # For simplicity, here's a basic approach using multiple queries (not the most efficient):
    users_cur = db.execute('SELECT id, name FROM users')
    users = users_cur.fetchall()
    for user in users:
        notes_cur = db.execute('SELECT content FROM notes WHERE user_id = ?', (user['id'],))
        user['notes'] = notes_cur.fetchall()
    return render_template('vartotojai.html', vartotojai=users)

@app.route('/uzrasai', methods=['GET', 'POST'])
def uzrasai():
    db = get_db()
    if request.method == 'POST':
        # This assumes you have a way to identify the current user's ID
        # For example, user_id = get_current_user_id()
        uzrasas = request.form.get('uzrasas')
        user_id = request.form.get('user_id')  # Placeholder for actual user identification logic
        if uzrasas and user_id:
            db.execute('INSERT INTO notes (content, user_id) VALUES (?, ?)', (uzrasas, user_id))
            db.commit()
            return redirect(url_for('uzrasai'))
    # Modify this query to join with the users table and fetch the username
    cur = db.execute('SELECT notes.content, users.name FROM notes JOIN users ON notes.user_id = users.id')
    uzrasai_listas = cur.fetchall()
    return render_template('uzrasai.html', uzrasai=uzrasai_listas)

if __name__ == "__main__":
    init_db()  # Ensure the database and tables are created
    app.run(debug=True)