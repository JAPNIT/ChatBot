from flask import Flask,render_template, url_for, redirect , request
import os.path, sqlite3
import datetime, time
from nltk.stem.wordnet import WordNetLemmatizer
import nltk, string, random

from api.ai import Agent
import json


#initialize the agent 
agent = Agent(
     'sakd',
     '04f67374d4b14ed68d9f13f70ddfdca8',
     '7b62bcd174784e09ab76acc96be378ed',
)


global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag, NoRecords
MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag, NoRecords = False, False, False, True
app = Flask(__name__)

def preprocessing(input_text):
    lst_stop_words=open("stop_words_and_singlish.txt", "r")
    stop_words=[]
    for line in lst_stop_words:
        stop_words.append(''.join(line.strip().split("\n")))
    lst_stop_words.close()

    translator_punc=str.maketrans('','', string.punctuation)
    words=input_text.translate(translator_punc)
    words = words.split() 
    noise_free_words = [word for word in words if word not in stop_words] 
    noise_free_text = " ".join(noise_free_words)

    word_result = []
    lem = WordNetLemmatizer()
    for w in noise_free_text:
        temp = lem.lemmatize(w)
        word_result.append(temp)
    new_words= ''.join(word_result)

    return new_words

def get_bot_response(input_text):
    global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag,NoRecords
    input_text = preprocessing(input_text)
    response = agent.query(input_text)
    result = response['result']
    fulfillment = result['fulfillment']

    if UpdateRecordsFlag:
        UpdateRecordsFlag = False
        try:
            value = float(input_text)
            if value < 0 or value > 20:
                raise ValueError
            if  value > 6.0 and  value < 4.0:
                ReminderFlag = True
                return "I take down liao. You are at MEDIUM risk, quite concern, go see doctor soon."
            elif value>=11.0 or value<=2.8:
                ReminderFlag = True
                return "I take down liao. You are at HIGH risk, alamak, you need to go see doctor now!"
            else:
                return "I take down liao. You are at NO risk. Healthy sia!"
        except:
            return "I dunno what you're talking about, please enter sugar level number."
        
    if fulfillment['speech'] == "update":
        UpdateRecordsFlag = True
    elif fulfillment['speech'] == "retrieve":
        RetrieveRecordsFlag = True
    return fulfillment['speech']


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
    global MedicalFlag, RetrieveRecordsFlag, UpdateRecordsFlag, NoRecords
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (request.form['text'], time.time(), "user", ))

        if UpdateRecordsFlag:
            db1 = get_db()
            val = request.form['text']
            try:
                val = float(val)
                now = datetime.datetime.today()
                date = now.strftime("%d") + "/" + now.strftime("%B") + "/" + now.strftime("%Y")
                db1.execute('INSERT INTO medicalrecords (timestamp, sugarlvl) VALUES (?,?)' , (date, request.form['text']))
                db1.commit()
                NoRecords = False
                
            except:
                pass

            db1.close()

            
        db.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (get_bot_response(request.form['text']), time.time(), "bot", ))
        db.commit()

        
        if RetrieveRecordsFlag:
            db1 = get_db()
            medrecords = db.execute('SELECT * FROM medicalrecords').fetchall()
            if NoRecords:
                db1.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', ("Sorry, no records found ah", time.time(), "bot", ))
                db1.commit()
            else:
                for rec in medrecords:
                    text = str(rec["timestamp"]) + ": " + str(rec["sugarlvl"]) + "mmol/L"
                    db1.execute('INSERT INTO chatbot (chat, timestamp, speaker) VALUES (?, ?, ?)', (text, time.time(), "bot", ))
                    db1.commit()
            RetrieveRecordsFlag = False
            db1.close()

            
        records = db.execute('SELECT * FROM chatbot').fetchall()
        db.close()
        return render_template('chat_bot.html', chat = records)
    
    else:
        medrecords = []
        db = get_db()
        records = db.execute('SELECT * FROM chatbot').fetchall()
        db.close()
        return render_template('chat_bot.html', chat = records)
    
if __name__ == '__main__':
    app.run(debug=True)
