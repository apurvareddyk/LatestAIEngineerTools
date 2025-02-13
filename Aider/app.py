from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    description = data['description']
    amount = data['amount']
    date = data['date']
    
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)', (description, amount, date))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = c.fetchall()
    conn.close()
    
    return jsonify(expenses)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
