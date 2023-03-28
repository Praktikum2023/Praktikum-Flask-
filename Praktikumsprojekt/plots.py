# Connecting to mysql database
import mysql.connector
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from PIL import Image
import pandas as pd 


#Funktion erstellt einen Barplot for ausgewählte Parameter
#Folgende Parameter werden verwendet:
#Cursor: Datatenbakcursor
#avg: Durschnittswert (bspw. Durschnittlicher Preis der Autos)
#var: Variable, die verglichen werden soll (bspw. Preis oder Reichweite oder ...)
#varindex: Stelle von var im Datensatz
#objectindex: Id von dem Auto, für das der Barplot erstellt werden soll 
#Name des Barplots
def create_barplot(cursor, avg, var, varindex, objectindex, tabellenname): 
    
    #Daten des Autos einlesen
    query = (" SELECT * from eautos ORDER BY %s ASC") % (var)
    cursor.execute(query)
    result = list(cursor.fetchall())
 
    #Daten aller Modelle in einen neuen Datensatz laden
    id = [i[25] for i in result]
    modell = [i[1] for i in result]
    var = [i[varindex] for i in result]

    data = {'id': id,
            'model': modell,
            'var': var}
    

    # Visualizing Data mit Matplotlib
    fig, ax = plt.subplots()
    bars = ax.bar(data['model'], data['var'])
    for i in range(len(bars)):
        if data['id'][i] == objectindex:
            bars[i].set_color('orange')

    ax.set_xlabel('Model')
    ax.set_ylabel('')
    ax.set_xticklabels([])
    ax.set_title(tabellenname)
    ax.axhline(y= avg, color='red')
    plt.show()
    
    # Bytes-Stream erstellen
    buf = io.BytesIO()

    # Plot in Bytes-Stream speichern
    plt.savefig(buf, format='png')

    # Bytes-Stream zurücksetzen
    buf.seek(0)

    plt.clf()

    return buf




