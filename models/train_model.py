import joblib
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os 

sys.path.append(os.path.abspath(".."))
from data.preprocessing import clean_text

# chargement du model avec joblib

X,y= joblib.load("../data/processed/processed.pkl")
vectorizer=joblib.load("../data/processed/vector.pkl")

#split

X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.2 ,random_state=42)


#model 1
model=MultinomialNB()
model.fit(X_train,y_train)

# predire avec le model

'''
ici on veut predire les labels en utilsant nos feedbacks comme entree
etant donne que le model connais la relation de probabilite entre ls feedbacks(entrees) et et les labels .
'''

y_pred=model.predict(X_test)

#evaluons l'accuracy du model

print(classification_report(y_pred,y_test))




#sauvegarde du model
joblib.dump(model, "../data/processed/model.pkl")

#exemple
def testing():

    
    text=input("entrez un texte ")
    cleaned =clean_text(text)
    vivi=vectorizer.transform([cleaned] )
    u =model.predict(vivi)
    return u

test=testing()
print(test)

    


