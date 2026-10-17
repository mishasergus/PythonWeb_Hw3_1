from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.json.ensure_ascii = False

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            destination TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            duration INTEGER NOT NULL,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_tours(name, min_price, max_price):
    conn = get_db_connection()

    query = '''SELECT * FROM tours WHERE name LIKE ? AND price >= ? AND price <= ? ORDER BY price'''
    if max_price == None:
        query = '''SELECT * FROM tours WHERE name LIKE ? AND price >= ? ORDER BY price'''
        search_name = f"%{name}%"
        tours = conn.execute(query, (search_name, min_price)).fetchall()
        conn.close()
        return tours
    search_name = f"%{name}%"
    tours = conn.execute(query, (search_name, min_price, max_price)).fetchall()
    conn.close()
    return tours

def add_tour(name, destination, description, price, duration, image_url):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tours (name, destination, description, price, duration, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, destination, description, price, duration, image_url))
    conn.commit()
    conn.close()


def seed_default_tours():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM tours').fetchone()[0]
    conn.close()

    if count == 0:
        default_tours = [
            ("Вікенд у Карпатах", "Україна", "Незабутній відпочинок у горах, підйом на Говерлу та чани.", 350.0, 4,
             "https://images.unsplash.com/photo-1519681393784-d120267933ba"),
            ("Магія Львова", "Україна", "Екскурсії старовинними вулицями, кав'ярні та шоколадні майстерні.", 200.0, 3,
             "https://images.unsplash.com/photo-1519167758481-83f550bb49b3"),
            ("Сонячний Париж", "Франція", "Романтична подорож до міста закоханих: Ейфелева вежа, Лувр та круїз Сеною.",
             850.0, 5, "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"),
            ("Античний Рим", "Італія", "Колізей, Ватикан та справжня італійська піца.", 750.0, 5,
             "https://images.unsplash.com/photo-1552832230-c0197dd311b5")
        ]

        for tour in default_tours:
            add_tour(*tour)
        print("Дефолтні тури успішно додано!")

init_db()
seed_default_tours()

@app.route('/')
def index():
    return render_template('main.html', active_page='index')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')


@app.route('/tours')
def tours():
    name = request.args.get('name', type=str) or ""
    min_price = request.args.get('min_price', type=float) or 0.0
    max_price = request.args.get('max_price', type=float) or None

    tours_list = get_tours(name, min_price, max_price)

    return render_template('tours.html',
                           tours=tours_list,
                           active_page='tours',
                           search_name=name,
                           min_price=min_price if min_price != 0.0 else "",
                           max_price=max_price if max_price is not None else "")

@app.route('/addTour', methods=['GET', 'POST'])
def addTour():
    if request.method == 'POST':
        name = request.form.get('name')
        destination = request.form.get('destination')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        duration = int(request.form.get('duration'))
        image_url = request.form.get('image_url')

        add_tour(name, destination, description, price, duration, image_url)
        return redirect(url_for('tours'))

    return render_template('addTour.html', active_page='add_tour')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', active_page='contacts')

if __name__ == '__main__':
    app.run(debug=True)

