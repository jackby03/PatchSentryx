import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Scan from './components/pages/scan/scan'; 
import Dashboard from './components/pages/dashboard/dashboard'
import './App.css';
import Inventory from './components/pages/inventory/inventory';

function App() {
  const [showRegister, setShowRegister] = useState(false);

  const toggleForm = () => {
    setShowRegister(!showRegister);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className={`app transition-container ${showRegister ? 'show-register' : 'show-login'}`}>
              {showRegister ? 
                <RegisterForm onLoginClick={toggleForm} /> : 
                <LoginForm onRegisterClick={toggleForm} />
              }
            </div>
          }
        />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/scan" element={<Scan />} />
        <Route path="/inventory" element={<Inventory />} />
      </Routes>
    </Router>
  );
}

export default App;