# mock_api.py
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

# Sample phone data
SAMPLE_DATA = [
    {
        "name": "Pixel 9 Pro",
        "brand": "Google",
        "release_date": "2024-10-01",
        "key_features": ["Tensor G4 chip", "200MP camera", "6.7" ,"LTPO OLED"]
    },
    {
        "name": "iPhone 16 Ultra",
        "brand": "Apple",
        "release_date": "2024-09-15",
        "key_features": ["A18 Bionic", "Under-display Face ID", "10x optical zoom"]
    },
    {
        "name": "Galaxy S25",
        "brand": "Samsung",
        "release_date": "2025-01-28",
        "key_features": ["Snapdragon 8 Gen 4", "200W fast charging", "AI Camera Suite"]
    }
]

@app.route('/new-phones')
def get_new_phones():
    # Simulate network delay (0-2 seconds)
    delay = request.args.get('delay', default=0, type=float)
    if delay > 0:
        time.sleep(delay)
    
    # Simulate random errors
    error_rate = request.args.get('error', default=0, type=float)
    if random.random() < error_rate:
        return jsonify({"error": "Server unavailable"}), 500
    
    # Return different status codes for testing
    status_code = request.args.get('status', default=200, type=int)
    if status_code != 200:
        return jsonify({"error": "Simulated error"}), status_code
    
    return jsonify(SAMPLE_DATA)

@app.route('/')
def health_check():
    return "Mock Phone API is running!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
