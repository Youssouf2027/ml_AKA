import pandas as pd
import re  
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import mysql.connector
import unicodedata
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import os
import sys


sys.path.append(os.path.abspath(".."))
from database import get_connection


stop_words=set(stopwords.words("french")+stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text: str):
    text=text.lower()
    text = re.sub(r"http\S+|www\S+", "", text) # Supprime les URLs
    text = re.sub(r"[@#]\w+", "", text) # Supprime les hashtags et les mentions
    text = re.sub(r"\d+", "", text) # Supprime les chiffres
    text = re.sub(r"[^\w\s]", "", text) # Supprime les caractères speciaux
    text = re.sub(r"\s+", " ", text).strip() # Supprime les espaces multiples
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore") # Supprime les accents
    words = text.split()
    words=[word for word in words if word not in stop_words ]
    
    words=[lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)



    '''
    pour bien lemmatizer les mots fraancais il est preferable d'utiliser spacy meilleur pour les librairies francais que wordnet

    pip install spacy
    python -m spacy download fr_core_news_sm

    import spacy
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]


    '''
    
def fetch_data_from_db():
    conn = get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT Feedback,sentiment,Id_category FROM Client_Query")
    sql= cursor.fetchall()
    return sql
    
def preprocess_data():
    data = fetch_data_from_db()
    df=pd.DataFrame(data, columns=["Feedback","sentiment","Id_category"])
    if df.empty:
        raise ValueError("Pas de données  dans la base")
    else:
        df["clean_feedbacks"]=df["Feedback"].astype(str).apply(clean_text)

        X_text= df["clean_feedbacks"]
        y=df["sentiment"]
        z=df["Id_category"]
        return X_text,y,z
    

    #vectorization des des feedbacks. TF-IDF

X_text,y,z=preprocess_data()

vectorizer= TfidfVectorizer(ngram_range=(1,2), max_features=5000)


X = vectorizer.fit_transform(X_text)

output="processed"
#sauvegarde avec le joblib
os.makedirs(output, exist_ok=True)
joblib.dump((X,y), f"{output}/processed.pkl")

joblib.dump((X,z), f"{output}/processed2.pkl")

joblib.dump(vectorizer, f"{output}/vector.pkl")

print(f"✅ Prétraitement terminé. Données sauvegardées dans {output}")


    

    


    
    


