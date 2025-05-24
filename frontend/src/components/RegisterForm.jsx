import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import "./RegisterForm.css";

const RegisterForm = ({ onLoginClick }) => {
  const [fullname, setFullname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    if (!fullname.trim() || !email.trim() || !password.trim()) {
      setError("Todos los campos son obligatorios.");
      return;
    }
    if (!emailRegex.test(email)) {
      setError("El correo electrónico no es válido.");
      return;
    }
    if (!passwordRegex.test(password)) {
      setError(
        "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y símbolos."
      );
      return;
    }

    try {
      const res = await fetch("http://localhost:3001/users?email=" + encodeURIComponent(email));
      const users = await res.json();
      if (users.length > 0) {
        setError("El correo electrónico ya está registrado.");
        return;
      }

      const id = uuidv4();

      const response = await fetch("http://localhost:3001/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, fullname, email, password }),
      });

      if (response.ok) {
        alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
        onLoginClick();
      } else {
        setError("Error al registrar usuario.");
      }
    } catch (err) {
      setError("Error de conexión con el servidor.");
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-overlay"></div>
      <div className="register-container">
        <div className="register-content">
          <h1 className="register-title">PatchSentryx</h1>
          <form onSubmit={handleRegister}>
            <div className="input-group">
              <input
                type="text"
                className="form-input"
                placeholder="Fullname"
                value={fullname}
                onChange={(e) => setFullname(e.target.value)}
                required
              />
            </div>
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
            {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
            <button className="register-submit-button" type="submit">
              Registrarse
            </button>
          </form>
          <div className="login-section">
            <p className="login-text">¿Ya tienes una cuenta?</p>
            <button className="login-link" onClick={onLoginClick}>
              Iniciar Sesión
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;