#Kleines script für das preprocessing der Strings der Originaldatenbank 

input_string = "Porsche,Taycan Turbo S Sport Tourismo,10/12,AWD,,190.620 €,160.185 €,15,97%,953 €,350 €,210 €,,93 kWh,240,458 km,295 km,,2.8 s,260 km/h,762 PS,560 kW,,23 min,,500 km,340 km,340 km,250 km,,2400 kg,405 l,,k.A.,k.A.,k.A.,k.A.,k.A."
# Zeichen, die entfernt werden sollen
remove_chars = ["€", "kWh", "km", "km/h", "PS", "kW", "min", "kg", "l", "%", "RWD", "AWD", "k.A."]

# Entfernen der Zeichen aus dem String
for char in remove_chars:
    input_string = input_string.replace(char, "")

# Ausgabe des neuen Strings
print(input_string)