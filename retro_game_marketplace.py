from pickle import TRUE
from flask import Flask, render_template, redirect, request, session
import psycopg2, os, bcrypt, requests

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=retro_marketplace')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key')

# url = "https://rawg-video-games-database.p.rapidapi.com/games"

# headers = {
# 	"X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com",
# 	"X-RapidAPI-Key": "88e0df8214764933a297e1f6dade78b1",
#     "?query=Elden Ring"
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
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

@app.route('/wishlist')
    

@app.route('/game_library')
def display_games():
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()
    cur.execute('SELECT id, image_url, name, price_in_cents, description, mobile FROM ads')
    
    results = cur.fetchall()
    names = []
    images = []
    prices = []
    mobile = []
    description = []
    print(results)
    for column in results:
        names.append(column[2])
        images.append(column[1])
        prices.append(column[3])
        description.append(column[4])
        mobile.append(column[5])
    length = len(names)
    return render_template('all_games.html',  id = id, names = names, images = images, prices = prices, length = length, mobile=mobile, description=description)

@app.route('/searched_library', methods=['POST'])
def dispay_searched_items():
    searched_word = request.form.get('searched')
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()
    cur.execute('SELECT id, image_url, name, price_in_cents FROM ads')
    results = cur.fetchall()
    names = []
    images = []
    prices = []
    id = []
    print(searched_word)
    for column in results:
        print(column[2])
        if searched_word in column[2]:
            id.append(column[0])
            names.append(column[2])
            images.append(column[1])
            prices.append(column[3])
    length = len(names)
    return render_template('searched_library.html',  id = id, names = names, images = images, prices = prices, length = length)

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():

    user_email = request.form.get('email')
    user_password = request.form.get('password')
    print(user_email)
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()

    cur.execute('SELECT id, email, name, password FROM users WHERE email = %s;', [user_email])
    results = cur.fetchone()
    name = results[2]
    email = results[1]
    id = results[0]
    password = results[3]
    valid = bcrypt.checkpw(user_password.encode(), password.encode())
    print(valid)
    conn.commit()
    conn.close()

    if results != None:
        if email == user_email and valid:
            session['name'] = name
            session['user_id'] = id
            return redirect('/')
        else:
            return redirect('/login')
    return redirect('/login')

@app.route('/logout')
def log_out():
  session.clear()
  return redirect('/')

@app.route('/signup')
def sign_up():
  return render_template('signup.html')

@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():

    user_email = request.form.get('email')
    user_password = request.form.get('password')
    user_name = request.form.get('name')
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()

    hash_pw = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    cur.execute('INSERT INTO users (email, password, name) VALUES (%s, %s, %s)', [user_email, hash_pw, user_name])
    conn.commit()
    conn.close()
    login_action()
    return redirect('/')

@app.route('/add_something')
def add_something():
  return render_template('add_something.html')

@app.route('/add_something_action', methods=['POST'])
def add_something_action():
    item = request.form.get('item')
    price = request.form.get('price')
    image = request.form.get('image')
    print(image)
    conn = psycopg2.connect('dbname=retro_marketplace')
    cur = conn.cursor()
    cur.execute('INSERT INTO ads (image_url, name, price_in_cents) VALUES (%s, %s, %s)', [image, item, price])
    conn.commit()
    conn.close()
    return redirect('/game_library')



if __name__ == "__main__":
    app.run(debug=True)