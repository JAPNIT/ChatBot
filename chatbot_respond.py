import nltk, string, random

#initialise
user_greet=input("Welcome to MEDIBot! Start with a greeting, or cancel: ")
user_respond="I want to view medical records."

#noise reduction/expression removal like "lah" and punctuation removal
lst_stop_words=open("stop_words_and_singlish.txt", "r")
stop_words=[]
for line in lst_stop_words:
    stop_words.append(''.join(line.strip().split("\n")))
lst_stop_words.close()

def _remove_noise(input_text):
    words = input_text.split() 
    noise_free_words = [word for word in words if word not in stop_words] 
    noise_free_text = " ".join(noise_free_words)
    translator_punc=str.maketrans('','', string.punctuation)
    noise_free_text=noise_free_text.translate(translator_punc)
    return noise_free_text

words=(_remove_noise(user_greet))

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

#greeting check? 
def response_greetings(greeting):
    greeting_file=open("Greetings.txt", "r")
    lst_greet=[]
    for line in greeting_file:
        lst_greet.append((''.join(line.strip('\n').split('\n'))))
    greeting_file.close()
    greeting=list(greeting.split())
    for i in range(len(greeting)):
        if greeting[i].lower() in ['hello', 'hi', 'hey', 'sup']:
            return random.choice(lst_greet)
        else:
            return ("Whoops, try a greeting instead!")

print(response_greetings(new_words))

#medical response
def response(user_response):
    user_response=list(user_response.split())
    for i in range(len(user_response)):
        if user_response[i].lower() in ['medical', 'record', 'records']:
            return "Your current records: " + "RECORDS"
        elif user_response[i].lower() in ['sugar', 'diabetic']:
            return "Your current status for DIABETES is: " + "diabetic/non" + "thus, SUGAR is " + "no/moderation"
    return "Anything else?"

responses=_remove_noise(user_respond)
print(response(responses))


