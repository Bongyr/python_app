from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, jsonify

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/ping')
def ping():
    return jsonify(message="pong")
    
@app.route('/')
def home():
    return "Hello, World!"
    
if __name__ == '__main__':
    app.run(debug=True host='0.0.0.0', port=5000)
