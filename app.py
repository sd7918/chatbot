import streamlit as st
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import pickle
import numpy as np
import json
import random

# Load the necessary data and models
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents1.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    # Tokenize the pattern - split words into an array
    sentence_words = nltk.word_tokenize(sentence)
    # Lemmatize each word - create a short form for the word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # Tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # Bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # Assign 1 if the current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # Filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Sort by the strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    result = "Sorry, I don't understand that."  # Default response if no matching tag is found
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = get_response(ints, intents)
    return res

st.title("Chatbot using Streamlit")

def chat():
    st.sidebar.title("Chat Log")
    chat_log = st.sidebar.empty()

    msg = st.text_input("You:", "")
    if st.button("Send") and msg != '':
        response = chatbot_response(msg)
        chat_log.text("You: " + msg)
        chat_log.text("Bot: " + response)
        st.text_input("You:", value ="", key="msg_input")

if __name__ == "__main__":
    chat()
