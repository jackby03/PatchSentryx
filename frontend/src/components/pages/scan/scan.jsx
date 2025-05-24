import React, { useEffect, useState } from "react";
import Sidebar from "../../sidebar/sidebar";
import "./scan.css";
import { createFirewall, getFirewalls, updateFirewall } from "../../../services/services";
import { useNavigate, useLocation } from "react-router-dom";

const initialState = {
  name: "",
  hostname: "",
  version: "",
  brand: "",
  model: "",
  serial_number: "",
  location: ""
};

const Scan = () => {
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");
  const [hasInventory, setHasInventory] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const userId = localStorage.getItem("userId");
    const firewallToEdit = location.state?.firewall;
    
    if (firewallToEdit) {
      setForm(firewallToEdit);
      setIsEditing(true);
    } else if (userId) {
      getFirewalls().then(firewalls => {
        const userFirewalls = firewalls.filter(fw => fw.collection_id === userId);
        setHasInventory(userFirewalls.length > 0);
      });
    }
  }, [location.state]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = localStorage.getItem("userId");
    if (!userId) {
      setError("No se encontró usuario autenticado.");
      return;
    }
    
    // Validar campos obligatorios
    for (let key in form) {
        if (
            key !== "id" &&
            (form[key] === undefined || form[key] === null || form[key] === "")
        ){
            setError("Todos los campos son obligatorios.");
            return;
        }
    }
    
    try {
      if (isEditing) {
        await updateFirewall(form);
      } else {
        await createFirewall(form, userId);
      }
      navigate("/inventory");
    } catch (err) {
      setError("Ocurrió un error al guardar el firewall. Por favor intenta nuevamente.");
      console.error("Error saving firewall:", err);
    }
  };

  return (
    <div className="scan-container">
      <Sidebar />
      <div className="scan-content">
        {!hasInventory || isEditing ? (
          <>
            <h2 style={{marginBottom: 24, color: "#2c3e50"}}>
              {isEditing ? "Editar Firewall" : "Registrar Firewall"}
            </h2>
            <form onSubmit={handleSubmit} className="firewall-form">
              <div>
                <label>Nombre</label>
                <input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: Firewall Principal"
                />
              </div>
              <div>
                <label>Hostname</label>
                <input
                  name="hostname"
                  value={form.hostname}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: fw-main.local"
                />
              </div>
              <div>
                <label>Versión</label>
                <input
                  name="version"
                  value={form.version}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: 1.0.0"
                />
              </div>
              <div>
                <label>Marca</label>
                <input
                  name="brand"
                  value={form.brand}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: Cisco"
                />
              </div>
              <div>
                <label>Modelo</label>
                <input
                  name="model"
                  value={form.model}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: ASA5506"
                />
              </div>
              <div>
                <label>Serial Number</label>
                <input
                  name="serial_number"
                  value={form.serial_number}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: SN123456789"
                />
              </div>
              <div>
                <label>Ubicación</label>
                <input
                  name="location"
                  value={form.location}
                  onChange={handleChange}
                  minLength={1}
                  maxLength={100}
                  required
                  placeholder="Ej: Data Center Lima"
                />
              </div>
              {error && <div style={{ color: "red", marginTop: 8 }}>{error}</div>}
              <button type="submit" className="add-provider-btn">
                {isEditing ? "Actualizar Firewall" : "Guardar Firewall"}
              </button>
              {isEditing && (
                <button 
                  type="button"
                  className="cancel-btn"
                  onClick={() => navigate("/inventory")}
                >
                  Cancelar
                </button>
              )}
            </form>
          </>
        ) : (
          <div>
            <h2>Ya tienes inventario registrado</h2>
            <button 
              className="add-provider-btn" 
              onClick={() => navigate("/inventory")}
            >
              Ver Inventario
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Scan;