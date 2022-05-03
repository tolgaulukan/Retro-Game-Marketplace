from flask import Flask, render_template, redirect, request, session
import psycopg2, os

DATABASE_URL = os.environ.get('DATABASE_URL', 'dbname=retro_marketplace')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key')

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

@app.route('/game_library')
def display_games():
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
    return render_template('all_games.html',  id = id, names = names, images = images, prices = prices, length = length)

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
  print(password)
  conn.commit()
  conn.close()

  if results != None:
    if email == user_email and password == user_password:
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


if __name__ == "__main__":
    app.run(debug=True)