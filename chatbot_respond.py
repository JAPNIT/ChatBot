import nltk, string, random

#initialise
user_respond="thanks a lot!!"

#noise reduction/expression removal like "lah" and punctuation removal
def preprocessing(input_text):

    def _remove_noise(input_text):
        lst_stop_words=open("stop_words_and_singlish.txt", "r")
        stop_words=[]
        for line in lst_stop_words:
            stop_words.append(''.join(line.strip().split("\n")))
        lst_stop_words.close()
        translator_punc=str.maketrans('','', string.punctuation)
        words=input_text.translate(translator_punc)
        words = words.split()
        noise_free_words = [word for word in words if word not in stop_words]
        print(noise_free_words)
        noise_free_text = " ".join(noise_free_words)
        return noise_free_text

    words=(_remove_noise(input_text))

    #word standardisation:
    phrases=open("singlish_phrases.txt", "r")
    singlish_phrases=[]
    for line in phrases:
        singlish_phrases.append(line.strip("\n").split(","))
    phrases.close()
    dic_singlish={x[0]:x[1] for x in singlish_phrases}

    def _lookup_words(input_text):
        words = input_text.split() 
        new_words = [] 
        for word in words:
            if word.lower() in dic_singlish:
                word = dic_singlish[word.lower()]
            new_words.append(word)
        new_text = " ".join(new_words) 
        return new_text

    new_words=_lookup_words(words)

    #lemmtising and stemming 
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk.stem.porter import PorterStemmer
    lem = WordNetLemmatizer()
    stem = PorterStemmer()

    word_result=[]
    for word in new_words:
        temp=lem.lemmatize(word)
        word_result.append(temp)

    new_words= ''.join(word_result)
    return new_words

#greeting check? 
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
        if input_text[i].lower() in ['medical', 'records', 'record']:
            return True
    return False


def check_blood_sugar(input_text):
    input_text=preprocessing(input_text)
    values=[]
    for i in range(len(input_text)):
        try:
            value=float(input_text[i]) #loses all precision?
            values.append(value)
        except:
            pass
        for j in range(len(values)):
            value=values[j]
            if  value > 6.0 and  value < 4.0:
                return "You are at: MEDIUM risk. Consult a medical professional."
            elif value>=11.0 or value<=2.8:
                return "You are at: HIGH risk. Please seek medical attention."
            return "You are at: NO risk. Keep it up!"
        
def farewell_check(input_text):
    input_text=preprocessing(input_text)
    goodbye_file=open("singlish_goodbyes.txt", "r")
    goodbye=[]
    for line in goodbye_file:
        goodbye.append((''.join(line.strip('\n').split('\n'))))
    goodbye_file.close()
    input_text=list(input_text.split())
    for i in range(len(input_text)):
        if input_text[i].lower() in ['thank', 'thanks', 'thk']:
            return random.choice(['Thank you ah!', 'Thanks ah!', 'No problem!'])
        elif input_text[i].lower() in ['bye', 'exit', 'see you', 'later', 'goodbye']:
            return random.choice(goodbye)
        else:
            return "I dunno what you're saying, try saying something again bah."
    


import datetime
if datetime.date.today().strftime('%A') == 'Friday':
    from datetime import datetime
    if datetime.now().strftime('%H:%M')=='14:44':
        print('Time to take your medication sia!')

print(preprocessing("Shiok ah!"))

