from flask import Flask, abort, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.urandom(24)
print("Secret key set:", app.secret_key)
csrf = CSRFProtect(app)

def calculate_financial_metrics(initial_loan, home_value, interest_rate, appreciation_rate, num_years=30):
    loan_balance = [initial_loan]
    home_values = [home_value]
    equity = [home_value - initial_loan]

    for _ in range(num_years - 1):
        new_loan = loan_balance[-1] * (1 + interest_rate / 100)
        new_home = home_values[-1] * (1 + appreciation_rate / 100)
        new_equity = new_home - new_loan

        loan_balance.append(new_loan)
        home_values.append(new_home)
        equity.append(new_equity)

    return loan_balance, home_values, equity

def calculate_metrics(initial_loan, home_value, interest_rate, appreciation_rate, years=30):
    metrics = []
    loan_balance = initial_loan
    current_home_value = home_value
    
    for year in range(years):
        # Calculate annual changes
        loan_balance += loan_balance * (interest_rate / 100)
        current_home_value += current_home_value * (appreciation_rate / 100)
        
        equity = current_home_value - loan_balance
        
        metrics.append({
            'Year': year + 1,
            'Loan_Balance': round(loan_balance, 2),
            'Home_Value': round(current_home_value, 2),
            'Equity': round(equity, 2)
        })
    
    return metrics

@app.route('/')
def home():
    print("Rendering index.html")
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        initial_loan = float(request.form['initial_loan'])
        home_value = float(request.form['home_value'])
        interest_rate = float(request.form['interest_rate'])
        appreciation_rate = float(request.form['appreciation_rate'])
        
        metrics = calculate_metrics(
            initial_loan,
            home_value,
            interest_rate,
            appreciation_rate
        )
        
        return render_template('results.html', metrics=metrics)
    else:
        return render_template('index.html') #redirect('/')


if __name__ == '__main__':
    app.run(debug=True)