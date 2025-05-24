import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";

const LoginForm = ({ onRegisterClick, animate }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim() || !password.trim()) {
      setError("Por favor, ingresa tu correo y contraseña.");
      return;
    }

    try {
      const res = await fetch(`http://localhost:3001/users?email=${encodeURIComponent(email)}`);
      const users = await res.json();

      if (users.length === 0) {
        setError("Correo o contraseña incorrectos.");
        return;
      }

      const user = users[0];
      if (user.password !== password) {
        setError("Correo o contraseña incorrectos.");
        return;
      }
      
      localStorage.setItem("userId", user.id);
      navigate("/dashboard");
    } catch (err) {
      setError("Error de conexión con el servidor.");
    }
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
            {error && (
              <div style={{ color: "red", marginBottom: 10 }}>{error}</div>
            )}
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