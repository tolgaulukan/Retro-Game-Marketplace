from flask import Flask, render_template, redirect, request, session
import psycopg2, os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()
    cur.execute('SELECT id, image_url, name, price_in_cents FROM ads')
    results = cur.fetchall()
    names = []
    images = []
    prices = []
    id = []
    for column in results:
        id.append(column[0])
        names.append(column[2])
        images.append(column[1])
        prices.append(column[3])
    length = len(names)
    return render_template('index.html', id = id, names = names, images = images, prices = prices, length = length)

@app.route('/game_library')
def display_games():
    return render_template('all_games.html')

if __name__ == "__main__":
    app.run(debug=True)