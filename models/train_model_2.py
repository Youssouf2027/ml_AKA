import joblib
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

X,z=joblib.load("data/processed/processed2.pkl")


X_train, X_test, Z_train, Z_test = train_test_split(X,z, test_size=0.2, random_state=42)

model_2=MultinomialNB()
model_2.fit(X_train,Z_train)

z_pred2=model_2.predict(X_test)

print(classification_report(z_pred2,Z_test))


joblib.dump(model_2, "data/processed/model2.pkl")

