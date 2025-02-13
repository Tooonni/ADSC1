import os
import glob
import sqlite3
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

# Pattern um nur die Pfade zubekommen aus den Input
# falls weitere Zeitungen aufgenommen werden soll, kann das Format weiter ausgeführt werden
PATTERN_FOR_FAZ = "**/*faz*.html"
PATTERN_FOR_SZ = "**/*sz*.html"
PATTERN_FOR_WELT = "**/*welt*.html"

os.chdir(Path(__file__).parent)

all_path_to_faz = glob.glob(os.path.join(Path.cwd().parent / "input", PATTERN_FOR_FAZ))
all_path_to_sz = glob.glob(os.path.join(Path.cwd().parent / "input", PATTERN_FOR_SZ))
all_path_to_welt = glob.glob(os.path.join(Path.cwd().parent / "input", PATTERN_FOR_WELT))
all_path = all_path_to_faz + all_path_to_sz + all_path_to_welt

# Funktion um Dictionary zu befüllen mit allen wichtigen Daten 
def get_news_data(file_path):
    #Datei wird eingelesen
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    bs = BeautifulSoup(html, "html.parser")
    filename = os.path.basename(file_path)  # Dateiname ziehen
    date = "-".join(filename.split("-")[:3])  # Datum aus Dateiname extrahieren
    parts_of_path = file_path.split(os.sep) # Dateiname durch / splitten
    path = os.path.join(parts_of_path[-2], parts_of_path[-1])   # hier werden nur die letzten 2 Endpoints gesichert aus dem Pfad
    
    data = []
    
    # Hier wird je nach Dateiname die ensprechenden Daten gezogen (Welcher Zeitung das ist/Name, der Pfad aus dem Input Ordner, Das Datum der Zeitung, Überschrift je nach Zeitung, Text je nach Zeitung aus der Überschrift)
    if "faz" in filename:
        teasers = bs.select(".top1-teaser__body-title, .teaser-object__title")
        for teaser in teasers:
            title = teaser.get_text(strip=True)
            text_element = teaser.find_next(class_="teaser-object__teaser-text")
            text = text_element.get_text(strip=True) if text_element else " "
            data.append({"Zeitung": "FAZ", "Pfad": path, "Datum": date, "Überschrift": title, "Text": text})
    
    elif "sz" in filename:
        articles = bs.find_all("article")
        for article in articles:
            title_element = article.select_one('[data-manual="teaser-title"]')
            title = title_element.get_text(strip=True) if title_element else " "
            text_element = article.select_one('[data-manual="teaser-text"]')
            text = text_element.get_text(strip=True) if text_element else " "
            data.append({"Zeitung": "SZ", "Pfad": path, "Datum": date, "Überschrift": title, "Text": text})
    
    elif "welt" in filename:
        articles = bs.find_all("article")
        for article in articles:
            title_element = article.select_one('.c-teaser__headline')
            title = title_element.get_text(strip=True) if title_element else " "
            text_element = article.select_one('.c-teaser__intro')
            text = text_element.get_text(strip=True) if text_element else " "
            data.append({"Zeitung": "Welt", "Pfad": path, "Datum": date, "Überschrift": title, "Text": text})
    
    return data

os.getcwd()

output_dir = Path.cwd().parent / "output"
all_data = []

for file_path in all_path:
    all_data.extend(get_news_data(file_path))

# DataFrame erstellen
df = pd.DataFrame(all_data)

# SQLite-Datenbank speichern
db_path = output_dir / "news_data.sqlite"
conn = sqlite3.connect(db_path)
df.to_sql("news", conn, if_exists="replace", index=False)
conn.close()

print(f"Datenbank gespeichert unter: {db_path}")