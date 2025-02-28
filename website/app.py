from flask import Flask, request, jsonify
from predict import predict_moisture, predict_drying_time

app = Flask(__name__)

@app.route('/api/predict_moisture', methods=['POST'])
def api_predict_moisture():
    data = request.get_json(force=True)
    sensor_data = data.get('sensor_data')
    if sensor_data is None:
        return jsonify({'error': 'sensor_data is required'}), 400
    moisture = predict_moisture(sensor_data)
    return jsonify({'predicted_moisture': moisture})

@app.route('/api/predict_drying', methods=['POST'])
def api_predict_drying():
    data = request.get_json(force=True)
    sensor_data = data.get('sensor_data')  # e.g., [temperature, humidity]
    predicted_moisture = data.get('predicted_moisture')
    if sensor_data is None or predicted_moisture is None:
        return jsonify({'error': 'sensor_data and predicted_moisture are required'}), 400
    drying_time = predict_drying_time(sensor_data, predicted_moisture)
    return jsonify({'predicted_drying_time': drying_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
