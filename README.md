# Zusammenfassung der Studienarbeit
Die Studie untersucht, ob sich die redaktionellen Strategien von FAZ, SZ und Welt in den veröffentlichten Artikeln widerspiegeln. Während die FAZ vor allem über Politik, Wirtschaft und Kultur berichtet, deckt die SZ ein breites Themenspektrum mit Schwerpunkten in Gesellschaft, Wissenschaft und Feuilleton ab. Die Welt wiederum konzentriert sich stark auf internationale Politik, Wirtschaft und Finanzen. Über einen Zeitraum von drei Monaten wurden täglich die Startseiten der drei Zeitungen mittels Web-Scraping erfasst, so dass insgesamt 276 HTML-Seiten mit 45.143 Artikeln analysiert wurden. Nach der Datenbereinigung wurde ein LDA-Modell trainiert, um thematische Schwerpunkte zu identifizieren. Die Ergebnisse zeigen, dass die FAZ vor allem politische und wirtschaftliche Themen behandelt, während die SZ eine größere Vielfalt aufweist und insbesondere soziale und kulturelle Inhalte betont. Die Welt zeichnet sich durch einen starken Fokus auf internationale Politik, Wirtschaft und Technologie aus. Die Hypothesen, dass die FAZ vor allem über Politik und Wirtschaft berichtet, die SZ eine größere Themenvielfalt mit den Schwerpunkten Gesellschaft und Wissenschaft aufweist und die Welt stärker über internationale Politik und Wirtschaft berichtet, konnten bestätigt werden. Insgesamt zeigt sich, dass die redaktionellen Strategien der Zeitungen in ihren Publikationen erkennbar sind.

Link zum Repo: https://github.com/Tooonni/ADSC1

# 1. Virtuelle Umgebung
- als erstes muss eine Virtuelle Umgebung erstellt werden
- in diesem Projekt wurde eine vituelle Umgebung mittels .venv erstellt
- falls virtualenv nicht installiert ist bitte ausführen: pip install virtualenv
- anschließend im Pfad des Projektes folgendes ausführen: python -m venv env
- dadurch wird im Projekt ein Ordner erstellt: "/.venv" (darin ist die virtuelle Umgebung)
- Um aus requirements.txt Packete zu installieren --> python -m pip install -r requirements.txt
- Um Packete direkt zu installieren --> python3 -m pip install PACKAGE_NAME
- Um alle Packages von venv zu bekommen --> python3 -m pip freeze

# 2. Daten laden
- die Daten sollten aus dem angegebenen OneDrive heruntergeladen werden: https://dbu-my.sharepoint.com/:f:/g/personal/marcel_hebing_dbuas_de/EjJVBqBSjmhApehlEABtn-kBhyNfwJMYeAM2kpKAi_XftA?e=RGWMdb
- je nach Bedarf, kann beliebige Monate heruntergeladen werden
- diese sollten jedoch aber im "/input" Ordner wie folgt abgelegt werden: "/input/data-lake_[JAHR]_[MONAT]

# 3. main.py ausführen
- beim Starten der main.py wird folgenes ausgeführt:
- es wird überprüft, ob die "news_data.sqlite" datei im "/output" Ordner vorhanden ist
- falls die nicht vorhanden ist, wird die "scripts/create_database.py" ausgeführt
    - dabei werden alle HTMLs geladen, die den Namen der Zeitungen angegeben wurden
    - anschließend wird je nach Zeitungsname die Atrikeln ausgelesen sowie der dazugehörige Text
    - abschließend werden die Daten (Zeitungsname, Pfad der HTML, Datum der Startseite, Überschrift, Text der Überschrift) in einer .sqlite im Ordner "/output" erstellt
- falls die vorhanden ist geht der Code weiter und ladet die "news_data.sqlite" und wandelt diese in einem DataFrame
- alle lehren Überschriften werden entfernt
- alle Wörter "Überschrift" und "Text" werden im DataFrame kleingeschrieben
- in "Überschrift" und "Text" werden alle Sonderzeichen bis auf "-" entfernt
- alle deutsche Stopword werden entfernt
- anschließend wird je Zeitung ein LDA ausgeführt
- es wird eine Grafik erstellt von den 3 Top Themen und eine Textdatei von den 10 Top Themen; beides wird in "/output" abgelegt