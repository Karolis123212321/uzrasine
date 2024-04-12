import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from datetime import datetime

DATABASE = 'application.db'

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Reikalingas saugoti sesijos duomenis

@app.context_processor
def inject_user():
    user = session.get('username', None)
    return dict(current_user=user)
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    date = datetime.strptime(value, format)
    return date.strftime(format)

app.jinja_env.filters['datetime'] = format_datetime

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setuser', methods=['POST'])
def setuser():
    session['username'] = request.form['username']
    return redirect(url_for('index'))



@app.route('/vartotojai', defaults={'user_name': None})
@app.route('/vartotojai/<user_name>')
def list_users(user_name):
    db = get_db()
    user_list_cur = db.execute('SELECT DISTINCT user_name FROM notes ORDER BY user_name')
    users = user_list_cur.fetchall()

    notes = None
    if user_name:
        notes_cur = db.execute('SELECT content, created_at FROM notes WHERE user_name = ? ORDER BY created_at DESC', (user_name,))
        notes = notes_cur.fetchall()

    return render_template('vartotojai.html', users=users, notes=notes, user_name=user_name)



@app.route('/uzrasai', methods=['GET', 'POST'])
def uzrasai():
    db = get_db()
    if request.method == 'POST':
        uzrasas = request.form.get('uzrasas')
        user_name = session.get('username')
        if uzrasas and user_name:
            db.execute('INSERT INTO notes (content, user_name) VALUES (?, ?)', (uzrasas, user_name))
            db.commit()
        return redirect(url_for('uzrasai'))
    cur = db.execute('SELECT content, created_at, user_name FROM notes ORDER BY created_at DESC')
    uzrasai_listas = cur.fetchall()
    return render_template('uzrasai.html', uzrasai=uzrasai_listas)

if __name__ == "__main__":
    init_db()  # Ensure the database and tables are created
    app.run(debug=True)