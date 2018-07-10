from flask import Flask,render_template, url_for, redirect , request
import os.path, sqlite3
import datetime, time

app = Flask(__name__)

def create_db():
    db = get_db()
    db.execute('CREATE TABLE chatbot (id INTEGER PRIMARY KEY AUTOINCREMENT, chat TEXT, timestamp TEXT, speaker TEXT)')
    print("created")
    db.close()

def get_db():
    db = sqlite3.connect('db.sqlite3')
    print("opened db")
    db.row_factory = sqlite3.Row
    return db
    
if not os.path.isfile('db.sqlite3'):
    create_db()

@app.route('/form', methods=['GET','POST'])
def form():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (request.form['text'], time.time(), "user", ) )
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', ("ok", time.time(), "bot", ) )
        db.commit()
        records = db.execute('SELECT * FROM chatbot').fetchall()
        db.close()
        return render_template('form.html', chat = records)
    else:
        return render_template('form.html', chat = [])
    
if __name__ == '__main__':
    app.run(debug=True)
