import React, { useState } from "react";
import "./LoginForm.css";

const LoginForm = ({ onRegisterClick, animate }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    alert("Inicio de sesión exitoso");
  };

  return (
    <div className="login-wrapper">
      <div className="login-overlay"></div>
      <div className="login-container">
        <div className={`login-content ${animate}`}>
          <h1 className="login-title">PatchSentryx</h1>
          <form onSubmit={handleLogin}>
            <div className="input-group">
              <input
                type="email"
                className="form-input"
                placeholder="Correo Electrónico"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                className="form-input"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button className="login-button" type="submit">
              Entrar
            </button>
          </form>
          <div className="register-section">
            <p className="register-text">
              Si no tienes cuenta, puedes crear una cuenta.
            </p>
            <button className="register-button" onClick={onRegisterClick}>
              Registrate
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;