from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
USERS_FILE = 'users.json'

# Function to load users from the JSON file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If the JSON file is empty or not properly formatted, return an empty dictionary
                return {}
    else:
        # If the JSON file does not exist, return an empty dictionary
        return {}

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', message='Username already exists')
        users[username] = password
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
        return redirect(url_for('home'))
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            return redirect(url_for('home'))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

# Route for the home page after login
@app.route('/home')
def home():
    return render_template('home.html')

# Route for user logout
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# Route for cart (orders)
@app.route('/cart')
def cart():
    return render_template('cart.html')

# Route for menu
@app.route('/menu')
def menu():
    return render_template('menu.html')
if __name__ == '__main__':
    app.run(debug=True)
