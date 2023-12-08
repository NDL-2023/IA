from flask import Flask, render_template, jsonify

# Load the tensorflow model
from tensorflow.keras.models import load_model
model = load_model('notre_model.keras')

@app.route('/api/emotions/')
def emotions():
    # get the text from the request
    text = request.args.get('text')
    # make the prediction
    prediction = model.predict(text)

    emotions = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']
    emotions_dict = {}


    for i in range(len(prediction)):
        emotions_dict[emotions[i]] = prediction[i]

    # 3 best emotions
    top_3 = sorted(emotions_dict.items(), key=lambda x: x[1], reverse=True)[:3]

    # return the prediction
    response = jsonify({
        'emotions': top_3
    })

    return response