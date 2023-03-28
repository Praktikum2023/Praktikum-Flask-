from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from getpass import getpass
import hashlib
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = secret_key
# Connecting to the Database
try:
  conn = mysql.connector.connect(host = 'localhost',
                                 user = 'root',# username  of the Database normally root 
                                 password = '',# password of the Database normally just blank 
                                 database = 'user_login'# name of the Database
                                 )
  # If the connection was a succes this messafe will be printed to terminal 
  if conn.is_connected():
    db_info = conn.get_server_info()
    print('Connected to Mysql server version ' ,db_info)
    
# If there is an error this message gets printed to your terminal    
except Error as e:
  print('An Error occured while connecting to MySQL', e)
  
  
  
@app.route('/')
def home():
  return render_template('login.html')
     

@app.route('/login', methods = ['POST', 'GET'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s AND email = %s", (username, hashed_password, email))
    user = cursor.fetchone()
    if user:
      session['username'] = username
      return redirect('/main_page')
    
    else:
      Error = 'Invalid username or password. Please try again.'
      return render_template('login', Error=Error)
  else:
    return render_template('register') 
  
@app.route('/main_page')
def main_page():  
  username = session['username']
  return render_template('main_page.html',  username = username) 

@app.route('/register', methods = ['POST', 'GET'])  
def register():
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      email = request.form['email']
      hashed_password = hashlib.sha256(password.encode()).hexdigest()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM accounts WHERE username = %s AND email = %s", (username, email))
      user = cursor.fetchone()
      if user:
        error = 'Username or email already exists. Please choose another Username or email.'
        return render_template('register.html', error=error)
      else:
        cursor.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        conn.commit()
        session['username'] = username
        return redirect('/')
  else: 
      return render_template('register.html')
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
  app.run(debug = True)