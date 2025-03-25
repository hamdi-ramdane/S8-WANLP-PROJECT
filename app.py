from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_fake_news, verify_source  # Import from predict.py

app = Flask(__name__)
CORS(app)  # Allows all origins (fine for development)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data['text']
        print(text)
        print("Predicting...")
        prediction = predict_fake_news(text)
        source_check = verify_source(text)
        return jsonify({"prediction": prediction, "source_check": source_check})
    except KeyError:
        return jsonify({"error": "Missing 'text' in request"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)