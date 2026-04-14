import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np



def load_data(filename):
    try:
        data = pd.read_csv(filename)
        print(f"Imported data successfully!\n", data, "\n")
        return data
    except FileNotFoundError: 
        print(f"Error: File 'fake_file.csv' not found.")
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
    except TypeError:
        print(f"{TypeError} has occurred\n")
# def predict_price():

def main():
    data = load_data("housing_data.csv")
    v_data = validate_data(data)
    train_model(v_data)
main() 

