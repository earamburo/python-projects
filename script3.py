import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def load_data(filename):
    try:
        data = pd.read_csv(filename)
        print(f"Imported data successfully!\n", data, "\n")
        return data
    except FileNotFoundError: 
        print(f"Error: File 'fake_file.csv' not found.")
        return None
def validate_data(data):
    try:
        print(f"First 5 row!\n{data.head()}\n")
        print(f"The data shape is\n{data.shape}\n")
        print(f"Checking data types\n{data.dtypes}\n")
        print(f"Checking if there are no null values in our data\n{data.isnull().sum()}\n")
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

           
        print("="*60)
        print("MODEL RESULTS")
        print("="*60)
        print(f"Coefficient (Slope): ${model.coef_[0]:,.2f} per sqft")
        print(f"Intercept: ${model.intercept_:,.2f}")
        print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
        print(f"\nModel Equation: Price = ${model.coef_[0]:,.2f} × Size + ${model.intercept_:,.2f}\n")

        return model, X, y, r2

    except TypeError:
        print(f"{TypeError} has occurred\n")
        return None, None, None, None
    except Exception as e:
        print(f"Error {e} has occurred")
        return None, None, None, None
def predict_price(model):
    try: 
        house_size_input = input(f"Enter the house size in square feet you would like an estimate for:\n")
        size = float(house_size_input)
        if(size <= 0):
            print(f"House size must be positive")
            return
        predicted_price = model.predict([[size]])[0]
        print(f"\nPrediction for a {size:,.0f} sqft house:")
        print(f"Estimated Price: ${predicted_price:,.2f}\n")
    except TypeError as e:
        print(f"{e} has occurred\n")
    except Exception as e:
        print(f"Error {e} has occurred")

def visualize_data(data):
    """Create scatter plot of the data."""
    try:
        print("="*60)
        print("CREATING VISUALIZATION")
        print("="*60)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(data['Size (sqft)'], data['Price ($)'], 
                   color='blue', alpha=0.6, s=100, edgecolors='black')
        
        plt.xlabel('House Size (sqft)', fontweight='bold')
        plt.ylabel('House Price ($)', fontweight='bold')
        plt.title('Housing Prices vs. House Size', fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        
        # Format y-axis with dollar signs
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        # CHANGE THIS PART - Save instead of show
        plt.savefig('scatter_plot.png', dpi=300, bbox_inches='tight')
        plt.close()  # Close the figure to free memory
        
        print("Scatter plot saved as 'scatter_plot.png'\n")
        print("Check your folder - the image file is ready to view!\n")
        
    except Exception as e:
        print(f"Error creating visualization: {e}")

def visualize_model(data, model, X, y):
    """Visualize the data points and regression line."""
    try:
        print("="*60)
        print("MODEL FIT VISUALIZATION")
        print("="*60)
        
        plt.figure(figsize=(10, 6))
        
        # Plot actual data points
        plt.scatter(X, y, color='blue', alpha=0.6, s=100, 
                   edgecolors='black', label='Actual Data', linewidth=1.5)
        
        # Plot regression line
        plt.plot(X, model.predict(X), color='red', linewidth=2, 
                label='Regression Line')
        
        plt.xlabel('House Size (sqft)', fontweight='bold')
        plt.ylabel('House Price ($)', fontweight='bold')
        plt.title('Linear Regression Model Fit', fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Format y-axis
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        plt.savefig('regression_plot.png', dpi=300, bbox_inches='tight')
        print("Regression plot saved as 'regression_plot.png'\n")        
        
        print("Model fit visualization displayed!\n")
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return



def main():
    # Load data
    print(f"WELCOME TO THE HOUSING PRICE PREDICTION PROGRAM!\n")
    print("="*60 + "\n")
    data = load_data("housing_data.csv")
    if data is None:
        print(f"Data did not load properly. Exiting Program")
        return
    
    v_data = validate_data(data)
    if v_data is None: 
        print(f"There are either null values or errors in your data, please review and try again. Goodbye")
        return
    
    # Visualize raw data
    visualize_data(v_data)

    # Train model
    trained = train_model(v_data)
    if trained[0] is None:
        print(f"Model training failed. Try again!")
        return
    
    model, X, y, r2 = train_model(v_data)


    visualize_model(v_data, model, X, y)
    while True:
        predict_price(model)

        again = input("Would you like to predict another price? (yes/no): ").lower()
        if again not in ['yes', 'y']:
            print("\nThank you for using the Housing Price Predictor!")
            break
main() 

