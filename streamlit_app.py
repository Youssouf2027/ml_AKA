import streamlit as st
import requests
import re




def verificateur_email(Email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, Email) is not None

st.title("Interface Utilisateur")

with st.form("feedback_form"):
    name=st.text_input("Nom:")
    age=st.number_input("Age:" ,min_value=10, max_value=100, step=1)
    sexe=st.selectbox("Sexe:",["Homme","Femme"])
    phone_number=st.number_input("Phone_number:")
    Email=st.text_input("email:")
    feedback=st.text_area("Votre feedback:")

    submitted=st.form_submit_button("Envoyer")

if submitted:
    if not verificateur_email(Email):
        st.error("E-mail inavalide. veuillez reessayer")
    else:
        st.success("merci pour votre feedback 🙏 ")

    
        


""" Sur quel fichier ? celu
C:Tu as testé l'affichage ? Normalement Streamlit est le dernier de nos fichiers

Y:je viens juste de faire le streamlit 
    j'ai voulu laiseer le backend app de fast api  la on allait faire ca ensemble 


C: Hannn mais tu as testé le visuel est bon ? C'est juste un formulaire non? Tu avais parlé preprocessing aussi

Y: strem??????

C: oui oui

Y: je l'affiche comme un fichier python aussi??

C: Normalement il y a une marniere de lancer streamlit avec uvicorn

Y: ok donc allons dedans on va voir ca ressemble a quoi

C: Azy lance

Y: mais yu peux voir mon terminal actu non


 
Y:regarde un peu le preprocessing et les resultat du model_train. cette  fois in a utilider classfication_report. 
 je savais pas que ca venais sous forme de table mm 

Allons dans preprocessing tu vas m'expliquer
""" 