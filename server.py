from flask import Flask, render_template, jsonify, request
import keras
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
#import translate
from translate import Translator

# Load the tensorflow model
from tensorflow.keras.models import load_model
# model = load_model('notre_model.keras')
model = keras.models.load_model('true_model.h5')
# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

app = Flask(__name__)
@app.route('/api/emotions/', methods=['POST'])
def emotions():
    data = request.get_json()
    if 'text' in data:
        text = data['text']
    else:
        return "ERROR: no text provided"
    
    #translate the text to english
    translator = Translator(to_lang="english", from_lang="french")
    print("TRANSLATE : ", translator.translate(text))

    emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']
    dict = {}
    text_seq = tokenizer.texts_to_sequences(text)
    text_padded = pad_sequences(text_seq, maxlen=200, padding='post', truncating='post')
    for i in range(len(emotions)):
        dict[emotions[i]] = model.predict(text_padded)[0][i]

    # 3 best emotions
    top_3 = sorted(dict.items(), key=lambda x: x[1], reverse=True)[:3]

    #reshaphe the top3 with only the emotion name
    top_3 = [x[0] for x in top_3]
    return jsonify(top_3)