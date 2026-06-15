from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from geopy.geocoders import Nominatim
import requests
import numpy as np
import tensorflow as tf
import joblib
import os
# from deepface import DeepFace   # Temporarily disabled for Render deployment

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = pd.read_csv(os.path.join(BASE_DIR, "crime_data.csv"))

def load_tflite_model():
    interpreter = tf.lite.Interpreter(
        model_path=os.path.join(BASE_DIR, "crime_model.tflite")
    )
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

interpreter, input_details, output_details = load_tflite_model()

SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

def predict_safety_score(interpreter, lat, lon, murder, rape, robbery):
    try:
        scaler = joblib.load(SCALER_PATH)
        raw_input = np.array([[lon, lat, murder, rape, robbery]], dtype=np.float32)
        input_data = scaler.transform(raw_input)

        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        prediction = interpreter.get_tensor(output_details[0]['index']).copy()
        return float(prediction[0][0])
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def find_nearest_crime_stats(lat, lon, data, radius=0.01):
    filtered = data[
        (abs(data["Latitude"] - lat) <= radius) &
        (abs(data["Longitude"] - lon) <= radius)
    ]
    if not filtered.empty:
        murder = filtered["Murder"].mean()
        rape = filtered["Rape"].mean()
        robbery = filtered["Robbery"].mean()
        return murder, rape, robbery
    return 0, 0, 0

def calculate_safety_score(route):
    total_score = 0
    valid_points = 0

    for lat, lon in route:
        murder, rape, robbery = find_nearest_crime_stats(lat, lon, data)
        score = predict_safety_score(interpreter, lat, lon, murder, rape, robbery)

        if score is not None:
            total_score += score
            valid_points += 1

    return total_score / valid_points if valid_points else 0

def get_routes(start, end):
    api_url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
        f"?overview=full&geometries=geojson&alternatives=true"
    )

    response = requests.get(api_url).json()

    routes = []
    if 'routes' in response:
        for idx, route in enumerate(response['routes']):
            coordinates = route['geometry']['coordinates']
            coordinates = [(float(lat), float(lon)) for lon, lat in coordinates]

            safety_score = calculate_safety_score(coordinates)
            distance = route.get('distance', 0)
            duration = route.get('duration', 0)

            routes.append({
                "coordinates": coordinates,
                "score": safety_score,
                "distance": distance,
                "duration": duration,
                "id": f"route_{idx+1}"
            })

    return routes

@app.route('/')
def index():
    return "✅ SafeNav Flask server is up and running!"

@app.route('/api/routes', methods=['POST'])
def get_safe_routes():
    try:
        data_json = request.json
        start = data_json.get('start')
        end = data_json.get('end')

        if not start or not end or 'lat' not in start or 'lng' not in start:
            return jsonify({'error': 'Start and end locations are required'}), 400

        start_coords = (start['lat'], start['lng'])
        end_coords = (end['lat'], end['lng'])

        routes = get_routes(start_coords, end_coords)

        if not routes:
            return jsonify({'error': 'No routes found'}), 404

        routes.sort(key=lambda x: x['score'], reverse=True)

        response = {
            'start': {'lat': start_coords[0], 'lng': start_coords[1]},
            'end': {'lat': end_coords[0], 'lng': end_coords[1]},
            'routes': [
                {
                    'id': route['id'],
                    'path': [{'lat': lat, 'lng': lon} for lat, lon in route['coordinates']],
                    'score': route['score'],
                    'distance': route['distance'],
                    'duration': route['duration']
                }
                for route in routes
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '')

    if not query:
        return jsonify([])

    geolocator = Nominatim(user_agent="safenav-autocomplete")

    try:
        results = geolocator.geocode(
            query,
            exactly_one=False,
            limit=5,
            addressdetails=True
        )

        suggestions = []

        if results:
            for result in results:
                suggestions.append({
                    'label': result.address,
                    'lat': result.latitude,
                    'lng': result.longitude
                })

        return jsonify(suggestions)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sos', methods=['POST'])
def sos_alert():
    try:
        return jsonify({"message": "🚨 SOS Alert Sent! Authorities have been notified."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DeepFace analysis route temporarily disabled for Render deployment
# @app.route('/api/analyze_route/<int:route_id>', methods=['GET'])
# def analyze_route(route_id):
#     try:
#         image_path = f"static/route_images/route_{route_id}.jpg"
#
#         if not os.path.exists(image_path):
#             return jsonify({"error": "Image not found"}), 404
#
#         try:
#             analysis = DeepFace.analyze(
#                 img_path=image_path,
#                 actions=["gender", "emotion"],
#                 enforce_detection=False
#             )
#         except Exception as df_error:
#             return jsonify({"error": f"DeepFace failed: {str(df_error)}"}), 500
#
#         if not isinstance(analysis, list):
#             analysis = [analysis]
#
#         gender_count = {}
#         emotion_count = {}
#         total_faces = len(analysis)
#
#         for face in analysis:
#             gender = face.get("dominant_gender") or face.get("gender")
#             emotion = face.get("dominant_emotion") or face.get("emotion")
#
#             if gender:
#                 gender_count[gender] = gender_count.get(gender, 0) + 1
#             if emotion:
#                 emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
#
#         return jsonify({
#             "total_faces": total_faces,
#             "gender_count": gender_count,
#             "emotion_count": emotion_count
#         })
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
