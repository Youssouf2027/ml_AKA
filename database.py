#Imports
import mysql.connector

# Connexion avec l'aide de mysql connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="AKA"
    )
    return conn

# Fetch toutes les reviews
'''
Consiste à recuperer tous les feedbacks utilisateurs avec les niveaux de confidence et leurs sentiments
'''
def get_new_feedback():
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT Id, Feedback FROM Client_Query WHERE classified=0 ")
    rows=cursor.fetchall()
    conn.close()
    return rows


# Fetch tous les clients
'''
Consiste à recuperer toutes les info concernant les clients
'''

def get_all_client(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Client_Information")
    myresult = cursor.fetchall()
    return myresult

# Fetch toutes les categories
'''
Consiste à recuperer toutes les categories
'''

def get_all_cat(conn):
    cursor = conn.cursor(dictionnary=True)
    cursor.execute("SELECT * FROM Category")
    myresult = cursor.fetchall()
    return myresult

# Creer un nouveau feedback
'''
Recuperer les données entrées des formulaires et les enregistrer dans la base de données
'''
def insert_feedback(nom: str, age: int, sexe: str,feedback: str, Phone_number: str, email:str ):

    conn=get_connection()
    cursor1=conn.cursor()
    cursor2 = conn.cursor()
    cursor1.execute( " INSERT INTO Client_Information(Name,Age,Sexe,Phone_number,E-mail) VALUES(%s, %s, %s, %s, %s)",
                    (nom, age, sexe, Phone_number,email ))
    
    cursor2.execute("INSERT INTO Client_Query(Feedback,Id_client) VALUES(%s,%s)",
                           (feedback,id_client,))
    conn.commit()
    conn.close()
    # return 




# Mettre a jour la confidence et le sentiment
'''
À partir des resultats du model, mettre à jour les points de sentiment et confidence
'''
def Update_sent_conf(predicted_sentiment, predicted_confidence,):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute( "UPDATE Client_Query SET sentiment=%s, confidence=%s ",
                   (predicted_sentiment, predicted_confidence))
    
# Testing
