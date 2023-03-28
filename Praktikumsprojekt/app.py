from flask import Flask, render_template, request, send_file, session, redirect
from flaskext.mysql import MySQL
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import plots
import art
import io
import mysql.connector
from mysql.connector import Error
import hashlib
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key
# Connecting to the Database
try:
  conn = mysql.connector.connect(host = 'localhost',
                                 user = 'root',# username  of the Database normally root 
                                 password = 'TP2023',# password of the Database normally just blank 
                                 database = 'praktikumsprojekt'# name of the Database
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


#app = Flask(__name__)


#Datenbankverbindung erstellen
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'TP2023'
app.config['MYSQL_DATABASE_DB'] = 'praktikumsprojekt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)



#Startseite erstellen
@app.route("/main_page")
def index():
     #Startseite rendern   
	return render_template("index.html")

@app.route("/filter", methods=["POST"])
def filter():
    #Variablen für Filterung aus der HTML-Datei importieren
    marke = request.form.get("marke")
    preis = request.form.get("preis")
    leistung = request.form.get("leistung")
    reichweite = request.form.get("reichweite")
    
    #Connection zur Datenbank abrufen und Cursor connecten
    conn = mysql.connect()
    cursor = conn.cursor()

    #Anfangsquery zur filterung der Daten initialisieren
    #Bedingung "WHERE 1=1 hinzufügen, damit bei Filterungsprozess die Anfangsquery durch AND ... ergänzt werden kann"
    query = "SELECT * FROM eautos WHERE 1=1"

    #Filterungsabfragen auf Basis der Variablen:
    if marke != "":
        query += f" AND Marke = '{marke}'"
    
    if preis != "":
        if preis == "lowPreis":
             query += f" AND Listenpreis < 50000 "
        if preis == "medPreis":
             query += f" AND Listenpreis < 100000 "
    
    if leistung != "":
        if leistung == "medLeistung":
             query += f" AND LeistungPS > 250 "
        if  preis == "highLeistung": 
             query += f" AND LeistungPS > 450 "
    
    if reichweite != "":
        if reichweite == "highReichweite":
             query += f" AND ReichweiteWLTP > 500 "

     #Daten auf Basis des Filterungsprozesses abrufen
    cursor.execute(query)
    results  = cursor.fetchall()
    conn.close()
    
    #Mit dem Daten die neue HTML-Seite aufrufen
    return render_template('filter.html', results=results)

@app.route('/create_image', methods=['POST'])
def create_image():
    
    # CarID des ausgewählen Modells abgreifen
    carid = request.form.get('carid')

    #Daten des ausgewählten Autos abrufen
    id = int(carid)
    objectindex = id 
    conn = mysql.connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM eautos WHERE id = {carid}"
    cursor.execute(query)

    #Daten des ausgewählten Autos in Results laden
    results  = cursor.fetchall()
    
    #Variablen zur Erstellung der Autokarte aus Results abspeicher
    marke = results[0][0]
    modell = results[0][1]
    preis = results[0][2]
    reichweite = results[0][7]
    
    #Passendes Autobild zu dem ausgewählten Auto auswählen
    carpic = "static/carpics/%d.png" % (id)

    if marke == "Skoda":
         logo = "static/logos/skodalogo.png"
    elif marke == "Audi":
         logo = "static/logos/audilogo.jpg"
    elif marke == "Porsche":
         logo = "static/logos/porschelogo.png"
    elif marke == "Skoda":
         logo = "static/logos/skodalogo.png"
    elif marke == "CUPRA":
         logo = "static/logos/cupralogo.png"
    else:
         logo = "static/logos/vwlogo.png"


    #Datenanalyse für  Vergleichsdiagramme: 
    query = "SELECT AVG(Listenpreis) FROM eautos;"
    cursor.execute(query)
    avgPreis  = cursor.fetchall()
    query = "SELECT AVG(ReichweiteWLTP) FROM eautos;"
    cursor.execute(query)
    avgReichweiteWLTP  = cursor.fetchall()
   
   
    #Diagramme erstellen
    #Dafür wird Funktion create_barplot aus der plots.py aufgerufen
    plotPreis = plots.create_barplot(cursor, avgPreis[0], "Listenpreis", 2, objectindex, "Preisvergleich")
    
    plotReichweite = plots.create_barplot(cursor, avgReichweiteWLTP[0], "ReichweiteWLTP", 7, objectindex, "Reichweitenvergleich")

    #Die Quartettkarte "Carcard" erstellen
    #Dafür wird die Funktion create_carcard aus der art.py aufgerufen
    carcard = art.create_carcard(plotPreis, plotReichweite, logo, carpic, marke, modell, preis, reichweite)

    # Setze den MIME-Typ
    mimetype = 'image/png'

     #Erstellte Carcard downloaden
    return send_file(carcard, as_attachment=True, mimetype=mimetype)
    

if __name__ == "__main__":
	app.run(debug=True)