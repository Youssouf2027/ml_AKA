import streamlit as st
import requests
import re




def verificateur_email(Email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, Email) is not None

st.title("Interface Utilisateur")

api_url = "http://127.0.0.1:3002/create_Feed"

with st.form("feedback_form"):
    name=st.text_input("Nom:")
    age=st.text_input("Age:")
    sexe=st.selectbox("Sexe:",["Homme","Femme"])
    phone_number=st.text_input("Phone_number:")
    Email=st.text_input("email:")
    feedback=st.text_area("Votre feedback:")

    submitted=st.form_submit_button("Envoyer")

payload = {
    "name": name,
    "age": age,
    "sexe": sexe,
    "phone_number": phone_number,
    "Email": Email,
    "feedback": feedback,
}

headers = {
    "Content-Type": "application/json" # Or other content type as required by your API
}

if submitted:
    if not verificateur_email(Email) or not name or not age  or not sexe or not phone_number or not Email or not feedback:
        st.error("Invalide. veuillez reessayer")
    else:
        st.success("merci pour votre feedback 🙏 ")
        try:
            response = requests.post( api_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            st.json(data)  # Display the JSON response

            if response.status_code == 200:
                result = response.json()
                st.success("working")
            else:
                st.error("not working")
            

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")

