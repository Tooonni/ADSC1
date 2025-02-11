# Info für virtuelle Umgebung (.venv)

- Um aus requirements.txt Packete zu installieren --> python3 -m pip install -r requirements.txt

- Um Packete direkt zu installieren --> python3 -m pip install PACKAGE_NAME

- Um alle Packages von venv zu bekommen --> python3 -m pip freeze


# Strategien der Zeitungne

- Strategie von:
    - FAZ _ Frankfurter Allgmeine = https://www.frankfurterallgemeine.de/die-faz
        - aus Wirtschaft, Politik und Kultur
    - SZ _ Süddeutsche Zeitung = https://www.sueddeutscher-verlag.de/sueddeutsche-zeitung
        - Aktuelles und Hintergründiges aus Ressort wie Politik, Wirtschaft, Feuilleton, Medien, Sport und Wissenschaft
    - WELT _ Welt = https://www.welt.de/services/article104636888/Impressum.html
        - Politik, Wirtschaft, Finanzen, Sport, Kultur, Wissenschaft, Literatur, Reise, Motor, Stil und Internet


# Schritte die gemacht werden müssen

- LDA nutzen um Content von Text zu erkennen
- Stopword nutzen um unnötige Wörter zu entfernen
- Bereinige den Text (HTML-Tags entfernen, Normalisierung).
- Verwende eine Technik wie LDA oder ein vortrainiertes Modell von Hugging Face, um Themen zu extrahieren.
- Gruppiere ähnliche Themen, wenn nötig, um die Hauptthemen pro Zeitung zu ermitteln.


# Schritte die gemacht werden/wurden

- Daten aus dem SharePoint laden und in input laden -> URL: https://dbu-my.sharepoint.com/:f:/g/personal/marcel_hebing_dbuas_de/EjJVBqBSjmhApehlEABtn-kBhyNfwJMYeAM2kpKAi_XftA?e=RGWMdb
- Extrahiere den Text aus der HTML-Seite
- Daten in einer SQLite3 Tabelle sichern --> WebScrapping Data Lake und Warehouse Beispiel ansehen
    - Tabellenformat: 
        - Name der Zeitschrift || Dateipfad (letzten 2 Endpoints) || Datum des Files || Überschrift || Text von der Überschrift