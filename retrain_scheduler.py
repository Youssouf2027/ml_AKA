import os
import schedule
import time


def retrain():
    print(" 🔄 .....re-entrainement du model..")
    os.system("python data/preprocessing.py")
    os.system("python train_model.py")
    print("-----------------------------------------------")
    print("model entrainé successfully!!")


schedule.every().day.at("").do(retrain)
print("⏳ Scheduler en cours d'exécution...")

while True:
    schedule.run_pending()
    time.sleep(60)