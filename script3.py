import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np



def load_data(filename):
    try:
        data = pd.read_csv(filename)
        print(f"Imported data successfully!\n", data, "\n")
        return data
    except FileNotFoundError: 
        print(f"Error: File 'fake_file.csv' not found.")
        retur None
def validate_data(data):
    try:
        print(f"First 5 row!\n{data.head()}\n")
        print(f"The data shape is\n{data.shape}\n")
        print(f"Checking data types\n{data.dtypes}\n")
        print(f"Checking if there are no null values in our data\n{data.isnull().sum()}\n")
        # print(data)
        return data
    except:
        print(f"An error has occurred!")

def train_model(data):
    try:
        print(f"Here is some data information\n{data.describe().astype(int)}\n")
        X = data['Size (sqft)'].values.reshape(-1, 1)
        y = data['Price ($)'].values
        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)

        return model, X, y, r2

    except TypeError:
        print(f"{TypeError} has occurred\n")
def predict_price():
    try: 
        r2 = r2_score(y, y_pred)
        print(f"The model predicted with an {r2} accuracy")
    except TypeError:
        print(f"{TypeError} has occurred\n")

def main():
    data = load_data("housing_data.csv")
    v_data = validate_data(data)
    train_model(v_data)
main() 

