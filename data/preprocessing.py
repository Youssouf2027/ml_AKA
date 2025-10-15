import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os
import re
from cleantext import clean
import spacy

# Ajouter le dossier parent pour l'import de database
import sys
path_to_db = os.path.abspath("")
sys.path.append(path_to_db)

from database import get_connection

# Charger modèle SpaCy pour le français
nlp = spacy.load("fr_core_news_sm")

# Stopwords français (spaCy gère déjà token.is_stop, mais on peut compléter)
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words("french"))

# -----------------------------
# Fonction de preprocessing
# -----------------------------
def preprocess_text(text: str, return_tokens: bool = False):
    """
    Nettoyage complet du texte :
    - Suppression URLs, mentions, chiffres, ponctuation, emojis
    - Mise en minuscule
    - Lemmatisation
    - Suppression stopwords
    - Tokenisation
    """

    # Nettoyage de base
    text = clean(
        text,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_digits=True,
        no_punct=True,
        no_emoji=True,
        lower=True
    )

    # Supprimer les caractères spéciaux restants
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", text)

    # Pipeline SpaCy
    doc = nlp(text)

    # Tokenisation + lemmatisation + suppression stopwords
    tokens = [
        token.lemma_
        for token in doc
        if token.is_alpha and not token.is_stop and token.lemma_ not in STOPWORDS and len(token) > 2
    ]

    if return_tokens:
        return tokens
    else:
        return " ".join(tokens)

# -----------------------------
# Récupération des données
# -----------------------------
def fetch_data_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Feedback, sentiment, Id_category FROM Client_Query")
    sql = cursor.fetchall()
    cursor.close()
    conn.close()
    return sql

# -----------------------------
# Prétraitement complet
# -----------------------------
def preprocess_data():
    data = fetch_data_from_db()
    df = pd.DataFrame(data, columns=["Feedback", "sentiment", "Id_category"])

    if df.empty:
        raise ValueError("Pas de données dans la base")
    
    # Appliquer preprocessing spaCy
    df["clean_feedbacks"] = df["Feedback"].astype(str).apply(preprocess_text)

    X_text = df["clean_feedbacks"]
    y = df["sentiment"]
    z = df["Id_category"]
    return X_text, y, z

X_text, y, z = preprocess_data()

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
X = vectorizer.fit_transform(X_text)

# Sauvegarde avec joblib
output = "data/processed"
os.makedirs(output, exist_ok=True)
joblib.dump((X, y), f"{output}/processed.pkl")
joblib.dump((X, z), f"{output}/processed2.pkl")
joblib.dump(vectorizer, f"{output}/vector.pkl")

print(f"Prétraitement terminé. Données sauvegardées dans {output}")
