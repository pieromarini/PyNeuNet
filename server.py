from flask import Flask, jsonify, render_template, request
from main import predict
import pickle


HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/predict-digit', methods=['POST'])
def digit():
    # Take the image and preprocess it.
    # predict and get the label
    # send the label as json to the template.
    if request.method == 'POST':
        img = request.get_json()

        # Load trained network file.
        with open('./trained-network', 'rb') as f:
            weights = pickle.load(f)

        digit, prob = predict(img, weights)
        data = {'digit': digit, 'prob': prob}
        return jsonify(data)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
