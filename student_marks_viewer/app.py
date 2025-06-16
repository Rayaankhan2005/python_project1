from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER,
            maths INTEGER,
            science INTEGER,
            english INTEGER
    
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        maths = request.form['maths']
        science = request.form['science']
        english = request.form['english']

        # Insert into DB
        conn = sqlite3.connect('student.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO students (name, roll, maths, science, english)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, roll, maths, science, english))
        conn.commit()
        conn.close()
        return redirect('/view')

    return render_template('add.html')


@app.route('/view')
def view_students():
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute('SELECT name, roll, maths, science, english FROM students')
    students = c.fetchall()
    conn.close()
    return render_template('view.html', students=students)



if __name__ == '__main__':
    init_db()  
    app.run(debug=True)


