import csv
import pandas as pd
import os.path

def saveDetails(name, email, age, gender, businessman):
    if os.path.isfile('data/user_details.csv'):
        with open('data/user_details.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows([[email, name, age, gender, businessman]])
    else:
        with open('data/user_details.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows([["email", "name", "age", "gender", "businessman"], [email, name, age, gender, businessman]])

def getDetails(email):
    try:
        df = pd.read_csv("data/user_details.csv")
        data = list(df[df["email"]==email].iloc[0])
        return data
    except Exception as e:
        return [-1]