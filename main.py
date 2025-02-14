import os
import sqlite3
import requests
import subprocess
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

OUTPUT_DIR = Path("output")
PATH_TO_SQLITE = OUTPUT_DIR / "news_data.sqlite"
CREATE_DB_SCRIPT = Path("scripts/create_database.py")
QUERY = "SELECT * FROM news"
STOPWORDS_URL = "https://raw.githubusercontent.com/solariz/german_stopwords/master/german_stopwords_full.txt"
PATH_PDF = os.path.join("output", "result.pdf")
PATH_TXT = os.path.join("output", "full_result.txt")

# Prüfen, ob die SQLite-Datei existiert
if not PATH_TO_SQLITE.exists():
    print(f"Datenbank '{PATH_TO_SQLITE}' nicht gefunden. Erstelle sie jetzt...")

    try:
        subprocess.run(["python3", str(CREATE_DB_SCRIPT)], check=True)
        print("Datenbank erfolgreich erstellt!")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")
        exit(1)  # Skript beenden, falls die DB nicht erstellt werden konnte
else:
    print(f"Datenbank '{PATH_TO_SQLITE}' gefunden. Prüfe Tabellen...")

connection = sqlite3.connect(PATH_TO_SQLITE)
df = pd.read_sql_query(QUERY, connection)

df.drop(df[df["Überschrift"] == " "].index, inplace=True)

df["Überschrift"] = df["Überschrift"].str.lower()
df["Text"] = df["Text"].str.lower()

df["Überschrift"] = df["Überschrift"].str.replace(r'[^a-zA-ZäöüÄÖÜß -]', '', regex=True)
df["Text"] = df["Text"].str.replace(r'[^a-zA-ZäöüÄÖÜß -]', '', regex=True)

stopwords = requests.get(STOPWORDS_URL, allow_redirects=True).text.split("\n")[9:]

def remove_stopwords(text, stopwords):
    # Den Text in Kleinbuchstaben umwandeln und dann in Wörter zerlegen
    words = text.lower().split()
    # Stopwords entfernen
    words = [word for word in words if word not in stopwords]
    # Die restlichen Wörter wieder zu einem Text zusammensetzen
    return " ".join(words)

df["Überschrift"] = df["Überschrift"].apply(lambda x: remove_stopwords(x, stopwords))
df["Text"] = df["Text"].apply(lambda x: remove_stopwords(x, stopwords))

df["text_combined"] = df["Überschrift"] + " " + df["Text"]

def perform_lda(df, n_topics=10):
    results = {}
    
    # Für jede Zeitung LDA ausführen
    for newspaper in df['Zeitung'].unique():
        # Filtere DataFrame nach Zeitung
        newspaper_df = df[df['Zeitung'] == newspaper]
        
        # CountVectorizer erstellen
        vectorizer = CountVectorizer(stop_words=stopwords)
        X = vectorizer.fit_transform(newspaper_df['text_combined'])
        
        # LDA Modell
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(X)
        
        # Extrahiere die Top Wörter für jedes Thema
        feature_names = np.array(vectorizer.get_feature_names_out())
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[:-11:-1]
            top_words = feature_names[top_words_idx]
            topics.append(" ".join(top_words))
        
        topic_distribution = lda.transform(X)
        # Durchschnitt über alle Dokumente
        avg_topic_distribution = topic_distribution.mean(axis=0)
        
        # Sortiere Topics nach Wahrscheinlichkeit & Indizes nach Wahrscheinlichkeit sortieren (absteigend)
        sorted_indices = np.argsort(avg_topic_distribution)[::-1]  # 
        
        sorted_topics = [topics[i] for i in sorted_indices]  # Sortierte Topics
        sorted_percentages = avg_topic_distribution[sorted_indices]  # Sortierte Wahrscheinlichkeiten
        sorted_percentages = (sorted_percentages / sorted_percentages.sum()) * 100  # In Prozent umrechnen
        
        # Ergebnisse speichern
        results[newspaper] = {"topics": sorted_topics, "percentages": sorted_percentages}
    
    return results

# LDA für das gesamte DataFrame durchführen
topics_by_newspaper = perform_lda(df)

def plot_top_topics(topics_by_newspaper, output_path):
    # Liste zur Speicherung der Daten für den Plot
    plot_data = []

    # Daten für jede Zeitung sammeln
    for newspaper, data in topics_by_newspaper.items():
        for i in range(3):  # Nur die Top 3 Topics nehmen
            plot_data.append({
                "Zeitung": newspaper,
                "Topic": f"{newspaper} - Topic {i+1}: {data['topics'][i]}",  # Zeitung + Topic Nummer
                "Wahrscheinlichkeit (%)": data["percentages"][i]
            })
    
    # DataFrame für die Visualisierung erstellen
    df_plot = pd.DataFrame(plot_data)

    # Stil setzen
    sns.set_theme(style="whitegrid")
    
    # Balkendiagramm mit Seaborn
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=df_plot, 
        x="Zeitung", 
        y="Wahrscheinlichkeit (%)", 
        hue="Topic",  # Hue enthält nun Zeitung + Topic
        palette="viridis"
    )
    
    # Titel & Labels
    plt.title("Top 3 Topics pro Zeitung", fontsize=14)
    plt.xlabel("Zeitung", fontsize=12)
    plt.ylabel("Wahrscheinlichkeit (%)", fontsize=12)
    plt.legend(title="Zeitung - Topic", bbox_to_anchor=(1, 1), loc='upper left')  # Legende mit Zeitung + Topic
    
    # Speichern als PDF
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()  # Figure schließen, um Speicher freizugeben

def save_text_results(topics_by_newspaper, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for newspaper, data in topics_by_newspaper.items():
            file.write(f"Top 10 Topics für {newspaper}:\n")
            for i, (topic, percentage) in enumerate(zip(data["topics"], data["percentages"]), 1):
                file.write(f"  Topic {i}: {topic} ({percentage:.2f}%)\n")
            file.write("\n")  # Leerzeile für bessere Lesbarkeit

# Funktionen ausführen und Ergebnisse speichern
plot_top_topics(topics_by_newspaper, PATH_PDF)
save_text_results(topics_by_newspaper, PATH_TXT)

print(f"Grafik gespeichert unter: {PATH_PDF}")
print(f"Textdatei gespeichert unter: {PATH_TXT}")