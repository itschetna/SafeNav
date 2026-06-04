# SafeNav - AI Powered Women Safety Navigation System

SafeNav is an AI-powered women safety navigation web application that helps users find safer travel routes based on crime data, location information, and route safety prediction. The project is designed to support safer movement by comparing route options and suggesting paths with better safety scores.

## Project Overview

The main idea behind SafeNav is to combine navigation with safety intelligence. Instead of only showing the shortest or fastest route, the system analyzes crime-related data and predicts a safety score for different routes. This helps users make more informed travel decisions, especially in unfamiliar or high-risk areas.

## Key Features

- Safe route recommendation based on crime data
- Multiple route options with safety scores
- Location search and autocomplete
- SOS alert functionality
- Crime-based safety prediction
- Backend APIs for route analysis and prediction
- Integration with routing and geolocation services

## My Contribution

I primarily handled the backend development of SafeNav. My work included building Flask-based REST APIs, integrating route generation services, processing crime datasets, implementing safety score prediction, and connecting the backend with machine learning components. I also worked on API debugging, input validation, error handling, and improving the overall backend flow to make route analysis more reliable.

## Tech Stack

### Backend
- Python
- Flask
- Flask-CORS
- TensorFlow Lite
- NumPy
- Pandas
- Joblib
- Geopy
- OSRM API

### Frontend
- React.js
- Tailwind CSS
- Axios
- React Router

### Machine Learning
- TensorFlow Lite model
- StandardScaler preprocessing
- Crime data-based safety scoring

## Backend APIs

### `/api/routes`
Returns multiple route options between source and destination locations along with safety scores.

### `/api/predict`
Predicts the safety level of a location or route segment using the trained machine learning model.

### `/api/autocomplete`
Provides location suggestions for user search queries.

### `/api/sos`
Simulates an emergency SOS alert feature.

## How It Works

1. The user enters source and destination locations.
2. The backend fetches possible routes using routing services.
3. Crime data near the route is analyzed.
4. The machine learning model predicts safety scores.
5. Routes are ranked based on safety and shown to the user.
6. The user can choose a safer route and access SOS support if needed.

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/itschetnasee/SafeNav.git
cd SafeNav
Backend Setup
cd backend
pip install -r requirements.txt
python app.py
Frontend Setup
cd frontend
npm install
npm start


### Future Improvements
Real-time crime alert integration
User authentication
Live location tracking
Trusted contact alert system
Mobile app version
More accurate route safety model
Deployment on cloud platforms
