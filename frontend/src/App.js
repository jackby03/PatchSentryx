import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css';

function App() {
  const [showRegister, setShowRegister] = useState(false);

  const toggleForm = () => {
    setShowRegister(!showRegister);
  };

  return (
    <div className={`app transition-container ${showRegister ? 'show-register' : 'show-login'}`}>
      {showRegister ? 
        <RegisterForm onLoginClick={toggleForm} /> : 
        <LoginForm onRegisterClick={toggleForm} />
      }
    </div>
  );
}

export default App;