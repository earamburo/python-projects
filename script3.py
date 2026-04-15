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
        x_mean = X.mean()
        x_centered = X - x_mean
        model = LinearRegression()
        model.fit(x_centered, y)

        y_pred = model.predict(x_centered)
        r2 = r2_score(y, y_pred)

           
        print("="*60)
        print("MODEL RESULTS")
        print("="*60)
        print(f"Coefficient (Slope): ${model.coef_[0]:,.2f} per sqft")
        print(f"Intercept: ${model.intercept_:,.2f}")
        print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
        print(f"Average house size: {x_mean:.0f} sqft")
        print(f"\nModel Equation: Price = ${model.coef_[0]:,.2f} × (Size - {x_mean:.0f}) + ${model.intercept_:,.2f}\n")

        return model, X, y, r2, x_mean, x_centered

    except TypeError:
        print(f"{TypeError} has occurred\n")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"Error {e} has occurred")
        return None, None, None, None, None, None
def predict_price(model, x_mean):
    try: 
        house_size_input = input(f"Enter the house size in square feet you would like an estimate for:\n")
        try: 
            size = float(house_size_input)
        except ValueError:
            print(f"Error {house_size_input} is not a valid number! Please enter a numeric value\n")
            return 

        if(size <= 0):
            print(f"House size must be positive")
            return
        size_centered = size - x_mean
        predicted_price = model.predict([[size_centered]])[0]
        print(f"\nPrediction for a {size:,.0f} sqft house:")
        print(f"Estimated Price: ${predicted_price:,.2f}\n")
    except TypeError as e:
        print(f"{e} has occurred\n")
    except Exception as e:
        print(f"Error {e} has occurred")

def visualize_data(data):
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

def visualize_model(data, model, X, y, x_mean):
    """Visualize the data points and regression line."""
    try:
        print("="*60)
        print("MODEL FIT VISUALIZATION")
        print("="*60)
        
        # Calculate R² score
        x_centered = X - x_mean
        y_pred = model.predict(x_centered)
        r2 = r2_score(y, y_pred)
        
        plt.figure(figsize=(10, 6))
        
        # Plot actual data points
        plt.scatter(X, y, color='blue', alpha=0.6, s=100, 
                   edgecolors='black', label='Actual Data', linewidth=1.5)
        
        # Plot regression line
        plt.plot(X, y_pred, color='red', linewidth=2, 
                label='Regression Line')
        
        plt.xlabel('House Size (sqft)', fontweight='bold')
        plt.ylabel('House Price ($)', fontweight='bold')
        plt.title('Linear Regression Model Fit (Centered)', fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper left')
        
        # Format y-axis
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # ADD THIS: Create text box with model statistics
        textstr = f'Model Statistics:\n'
        textstr += f'Slope: ${model.coef_[0]:,.2f}/sqft\n'
        textstr += f'Intercept: ${model.intercept_:,.2f}\n'
        textstr += f'R² Score: {r2:.4f} ({r2*100:.2f}%)'
        
        # Place text box in lower right corner
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.98, 0.05, textstr, transform=ax.transAxes, 
                fontsize=10, verticalalignment='bottom', 
                horizontalalignment='right', bbox=props)
        
        plt.tight_layout()
        plt.savefig('regression_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Regression plot saved as 'regression_plot.png'\n")        
        print("Model statistics are shown in the plot!\n")
        
    except Exception as e:
        print(f"Error creating visualization: {e}")


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
    model, X, y, r2, x_mean, x_centered = train_model(v_data)
    if model is None:
        print(f"Model training failed. Try again!")
        return


    visualize_model(v_data, model, X, y, x_mean)
    while True:
        predict_price(model, x_mean)

        again = input("Would you like to predict another price? (yes/no): ").lower()
        if again not in ['yes', 'y']:
            print("\nThank you for using the Housing Price Predictor!")
            break
main() 

