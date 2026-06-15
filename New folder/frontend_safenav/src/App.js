import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from "axios";
import SafeMap from "./components/safemap.jsx";
import RouteCard from "./components/RouteCard.jsx";
import SearchBox from "./components/SearchBox.jsx";
import MoodAnalysis from "./components/MoodAnalysis.jsx";
import Hero from "./components/Hero.jsx";
import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
import FAQ from "./components/FAQ.jsx";
import PhoneFrame from './components/PhoneFrame.jsx';
import Features from './components/Features.jsx';
import AboutUs from "./components/AboutUs.jsx";

const API_BASE_URL = "https://safenav-us1k.onrender.com";

const Dashboard = () => (
  <div className="mobile-dashboard">
    <div className="mobile-hero" style={{ maxHeight: '30vh', overflow: 'hidden' }}>
      <Hero />
    </div>
    <Features />
  </div>
);

const SOS = () => {
  const handleSendSOS = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/sos`);
      alert(response.data.message || "SOS Sent! Authorities have been notified.");
    } catch (error) {
      alert("Failed to send SOS. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md p-8 bg-white rounded-lg shadow-lg text-center">
        <h2 className="text-3xl font-bold mb-6 text-red-600">SOS</h2>
        <p className="text-gray-700 mb-8">Click the SOS button in case of emergency. Authorities will be notified.</p>
        <button
          onClick={handleSendSOS}
          className="mt-4 bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg shadow-md transition duration-300 ease-in-out button-with-label"
        >
          Send SOS
        </button>
      </div>
    </div>
  );
};

const RouteFinder = () => {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [routes, setRoutes] = useState([]);
  const [error, setError] = useState("");

  const fetchRoutes = async () => {
    if (!start || !end) {
      setError("Start and end locations are required");
      return;
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/api/routes`, {
        start,
        end,
      });

      setRoutes(response.data.routes);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong");
      setRoutes([]);
    }
  };

  return (
    <div className="px-6 pt-24 pb-10 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold text-center mb-8 text-blue-700">SafeNav Route Finder</h2>

      <div className="bg-white shadow-lg rounded-lg p-6 max-w-3xl mx-auto">
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <SearchBox
            placeholder="Enter Start Location"
            onSelect={(location) => setStart({ lat: location.lat, lng: location.lng })}
          />
          <SearchBox
            placeholder="Enter End Location"
            onSelect={(location) => setEnd({ lat: location.lat, lng: location.lng })}
          />
        </div>

        <button
          onClick={fetchRoutes}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded w-full"
        >
          Find Safe Route
        </button>

        {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
      </div>

      {routes.length > 0 && (
        <div className="mt-12 max-w-6xl mx-auto">
          <h3 className="text-2xl font-semibold mb-4 text-gray-800">Available Routes:</h3>

          <div className="grid md:grid-cols-2 gap-6">
            {routes.slice(0, 2).map((route, idx) => (
              <RouteCard
                key={idx}
                route={route}
                index={idx}
                label={idx === 0 ? "Safest Route" : "Fastest Route"}
              />
            ))}
          </div>

          <div className="mt-10">
            <SafeMap routes={routes} />
          </div>
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <Router>
        <PhoneFrame>
          <div className="phone-content">
            <Navbar />
            <div className="phone-body" style={{ paddingTop: '60px', paddingBottom: '60px' }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/route" element={<RouteFinder />} />
                <Route path="/mood-analysis" element={<MoodAnalysis />} />
                <Route path="/sos" element={<SOS />} />
                <Route path="/faq" element={<FAQ />} />
                <Route path="/about" element={<AboutUs />} />
              </Routes>
            </div>
            <Footer />
          </div>
        </PhoneFrame>
      </Router>
    </div>
  );
}

export default App;
