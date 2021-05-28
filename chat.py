import speech_recognition as sr
import sqlite3
# import webbrowser
import playsound
import os
from gtts import gTTS
from time import ctime
import time


r = sr.Recognizer()
#---------------------------

import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# bot_name = "Sam"
print("Let's chat! type 'quit' to exit")
#-------------------------------------------------------------

def record_audio(ask = False):
    with sr.Microphone() as source:     
        audio = r.listen(source)       
        voice_data = ''

        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            alexis_speak('sorry, I did not get that')
        except sr.RequestError:
            alexis_speak('sorry, my speech service is down')
        return voice_data


def alexis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)



#if 'exit' in voice_data:
        #alexis_speak('I am glad to help you, thank you for using chatrobot')
        #exit()
#-------------------------------------------------------------

alexis_speak('Hi, How can I help you?')

i = 0
m = 0
doneName = 0
while True:
    
    sentence = record_audio() # input('You: ')
    value_sentence = sentence
    if  sentence == "quit" or 'exit' in sentence:
        alexis_speak('I am glad to help you, thank you for using chatrobot')
        break
    
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                alexis_speak(f"{random.choice(intent['responses'])}") 
    else:
        alexis_speak(f"I do not understand...")

    '''if "what is your name" in value_sentence:
        alexis_speak('what is your name')
        sentence = record_audio()  

        if "my name is" in sentence or "i am" in sentence:
            doneName+=1
            name = sentence.split(" ") 
            theName = name[-1]
            alexis_speak("The name {} is beautiful".format(theName))                    
    else:
        i+=1

    if doneName != 0:     
        doneName-=1
        alexis_speak('How old are you')
        sentence = record_audio()
        if "years old" in sentence or "i am" in sentence or sentence.isdigit()==True:            
            c = ''.join([n for n in sentence if n.isdigit()])  
            print(c)
            theAge = int(c)
            if theAge in range(130):    
                if theAge < 18 :
                    alexis_speak('You are still young, You still have time to develop yourself.')
                if theAge >= 18 and theAge < 45:
                    alexis_speak("You are in your youth, make your effort, as the future of the nation depends on you.")
                if theAge > 45:
                    alexis_speak("You must have become very now. I hope that you have fulfilled your dreams, the role now for your children.")
            else:
                alexis_speak("your age is not logical")
        else:
            i+=1
  
    
    if i != 0:
        i-=1
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    alexis_speak(f"{random.choice(intent['responses'])}") 
        else:
            alexis_speak(f"I do not understand...")
        i-=1

    con = sqlite3.connect("info.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE if not exists pepole (first_name TEXT, last_name TEXT,telephone INT, age INT)")

    con.execute("INSERT INTO pepole VALUES ('{}','bani issa','565656','{}')".format(theName, theAge))
    con.commit()
    con.close()'''