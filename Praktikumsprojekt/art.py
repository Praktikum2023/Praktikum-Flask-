from PIL import Image, ImageDraw, ImageFont, ImageOps
import tempfile


#Create_carcard erstellt die finale Quartettkarte, die später gedownladed wird
#Parameter:
#grafik1: Erstes Balkendiagramm, was zuvor erstellt wurde
#grafik2: Zweites Balkendiagramm, was zuvor erstellt wurde
#logo: Logo der Automarke
#carPic: Bild des Autos
#modell: Modellname des Autos
#preis: Preis des Autos
#reichweite: Reichweite des Autos

def create_carcard(grafik1, grafik2, logo, carPic, marke, modell, preis, reichweite):
    #Leeres Bild initialisieren
    image = Image.new("RGB", (1200, 800), (255, 255, 255))
    # Erstelle eine Zeichenfläche, um Text hinzuzufügen
    draw = ImageDraw.Draw(image)
    # Definiere den Text und die Schriftart
    schluessel = "Marke: \nModell: \nPreis: \nReichweite: " 
    params = " %s\n %s\n %d€\n %dkm" % (marke, modell, preis, reichweite)
    font = ImageFont.truetype("arial.ttf", 30)
    
    #Rahmengröße festlegen
    border_size = 10

    #Grafiken öffenen und auf die richtige Größe bringen und einen Rahmen hinzufügen
    graphic1 = Image.open(grafik1)
    graphic1 = graphic1.resize((500,400))
    graphic1 = ImageOps.expand(graphic1, border=border_size, fill='black')
    graphic2 = Image.open(grafik2)
    graphic2 = graphic2.resize((500,400))
    graphic2 = ImageOps.expand(graphic2, border=border_size, fill='black')

    #Logo und Autobild öffenen und auf richtige Größe Bringen
    logo = Image.open(logo)
    logo = logo.resize((200,200))
    carpic = Image.open(carPic)
    carpic = carpic.resize((430,220))
    carpic = ImageOps.expand(carpic, border=border_size, fill='black')

    # Text, Grafiken und Bilder auf das Bild "Drucken"
    draw.text((120, 300), schluessel, font=font, fill=(0, 0, 0))
    draw.text((330, 300), params, font=font, fill=(0, 0, 0))
    image.paste(graphic1, (700, -10))
    image.paste(graphic2, (700, 400))
    image.paste(logo, (250, 30))
    image.paste(carpic, (120,550))

    #Trennlienien zwischen Textbereichen hinzufügen
    draw.line((0, 250, 700, 250), fill=(0, 0, 0), width=5)
    draw.line((0, 500, 700, 500), fill=(0, 0, 0), width=5)

    # Zeige das Bild
    #image.show("my_image.png")

    #Temporäre Bilddatei für den späteren Download bereitstellen
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        image.save(f, format='PNG')
        temp_file_path = f.name
    
    return temp_file_path



