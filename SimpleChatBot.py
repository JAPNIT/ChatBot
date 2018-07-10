from flask import Flask,render_template, url_for, redirect , request
import os.path, sqlite3
import datetime, time
from nltk.stem.wordnet import WordNetLemmatizer
import nltk, string, random

global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag
MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag = False, False, False
app = Flask(__name__)

def preprocessing(input_text):
    lst_stop_words=open("stop_words_and_singlish.txt", "r")
    stop_words=[]
    for line in lst_stop_words:
        stop_words.append(''.join(line.strip().split("\n")))
    lst_stop_words.close()

    words = input_text.split() 
    noise_free_words = [word for word in words if word not in stop_words] 
    noise_free_text = " ".join(noise_free_words)
    translator_punc=str.maketrans('','', string.punctuation)
    noise_free_text=noise_free_text.translate(translator_punc)

    word_result = []
    lem = WordNetLemmatizer()
    for w in noise_free_text:
        temp = lem.lemmatize(w)
        word_result.append(temp)
    new_words= ''.join(word_result)

    return new_words

def greeting_check(input_text):
    input_text = preprocessing(input_text) 
    greeting=list(input_text.split())
    for i in range(len(greeting)):
        if greeting[i].lower() in ['hello', 'hi', 'hey', 'supp']:
            return True
    return False

def medical_check(input_text):
    input_text = preprocessing(input_text)
    input_text=list(input_text.split())
    for i in range(len(input_text)):
        if input_text[i].lower() in ['medical', 'records', 'diabetes', 'sugar level']:
            return True
    return False

def get_bot_response(input_text):
    global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag
    if medical_check(input_text): #function
        MedicalFlag = True
        return "Do you want to retrieve existing or update?"
    elif MedicalFlag == True:
        if input_text == "retrieve":
            RetrieveRecordsFlag = True
            return "Retrieving records now :)"
        elif input_text == "update":
            UpdateRecordsFlag = True
            return "Tell me your sugar level"
        
    if greeting_check(input_text):
        greeting_file=open("Greetings.txt", "r")
        lst_greet=[]
        for line in greeting_file:
            lst_greet.append((''.join(line.strip('\n').split('\n'))))
        greeting_file.close()
        return random.choice(lst_greet)
    else:
        return "I don't understand"














def create_db():
    db = get_db()
    db.execute('CREATE TABLE chatbot (id INTEGER PRIMARY KEY AUTOINCREMENT, chat TEXT, timestamp TEXT, speaker TEXT)')
    db.execute('CREATE TABLE medicalrecords (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, sugarlvl TEXT)')
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
    global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (request.form['text'], time.time(), "user", ))
        
        if UpdateRecordsFlag:
            now = datetime.datetime.now()
            date = now.day + now.month + now.year #fix date
            db.execute('INSERT INTO medicalrecords (timestamp, sugarlvl) VALUES (?,?)' , (date, request.form['text']))
            db.commit()
            UpdateRecordsFlag = False
            MedicalFlag = False
            
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (get_bot_response(request.form['text']), time.time(), "bot", ))
        db.commit()
        
        if RetrieveRecordsFlag:
            medrecords = db.execute('SELECT * FROM medicalrecords').fetchall()
            for rec in medrecords:
                text = str(rec["timestamp"]) + " " + str(rec["sugarlvl"])  
                db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (text, time.time(), "bot", ))
                db.commit()
            RetrieveRecordsFlag = False
            MedicalFlag = False
            
        
        records = db.execute('SELECT * FROM chatbot').fetchall()
        db.close()
        return render_template('form.html', chat = records)
    else:
        medrecords = []
        db = get_db()
        records = db.execute('SELECT * FROM chatbot').fetchall()
        db.close()
        return render_template('form.html', chat = records)
    
if __name__ == '__main__':
    app.run(debug=True)
