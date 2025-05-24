import React, { useEffect, useState } from 'react';
import './inventory.css';
import Sidebar from '../../sidebar/sidebar';
import { getFirewalls, deleteFirewall } from '../../../services/services';
import { useNavigate } from 'react-router-dom';

const Inventory = () => {
  const [firewalls, setFirewalls] = useState([]);
  const [search, setSearch] = useState("");
  const [date, setDate] = useState("");
  const [selected, setSelected] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadFirewalls();
  }, []);

  const loadFirewalls = () => {
    const userId = localStorage.getItem("userId");
    getFirewalls().then(allFirewalls => {
      setFirewalls(allFirewalls.filter(fw => fw.collection_id === userId));
    });
  };

  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de eliminar este firewall?")) {
      await deleteFirewall(id);
      loadFirewalls();
    }
  };

  const handleEdit = (firewall) => {
    navigate('/scan', { state: { firewall } });
  };

  const filtered = firewalls.filter(fw => {
    const matchesSearch = fw.name.toLowerCase().includes(search.toLowerCase());
    const matchesDate = date ? fw.created_at && fw.created_at.startsWith(date) : true;
    return matchesSearch && matchesDate;
  });

  return (
    <div className="inventory-container">
      <Sidebar />
      <div className="inventory-content inventory-content-right">
        <div className="inventory-header">
          <h2>Firewall Inventory</h2>
        </div>
        <div className="search-filters search-filters-below">
          <div className="search-box">
            <input
              type="text"
              placeholder="Buscar por nombre..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <svg className="search-icon" viewBox="0 0 24 24">
              <path d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
          </div>
          <input
            type="date"
            value={date}
            onChange={e => setDate(e.target.value)}
            className="date-filter"
          />
        </div>

        <div className="inventory-grid">
          {filtered.length > 0 ? (
            <div className="site-cards">
              {filtered.map(fw => (
                <div key={fw.id} className="site-card">
                  <div className="card-header">
                    <h3>{fw.name}</h3>
                    <div className="card-actions">
                      <button 
                        className="edit-btn"
                        onClick={() => handleEdit(fw)}
                      >
                        Edit
                      </button>
                      <button 
                        className="delete-btn"
                        onClick={() => handleDelete(fw.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                  <div className="card-details">
                    <div className="detail-row">
                      <span className="detail-label">Brand:</span>
                      <span>{fw.brand}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Model:</span>
                      <span>{fw.model}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Location:</span>
                      <span>{fw.location}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Last Scan:</span>
                      <span>{fw.created_at ? new Date(fw.created_at).toLocaleString() : "N/A"}</span>
                    </div>
                  </div>
                  <button 
                    className="view-details-btn"
                    onClick={() => setSelected(fw)}
                  >
                    View Details
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-inventory">
              <p>No hay registros en el inventario, por favor registra uno.</p>
              <button 
                className="add-firewall-btn" 
                onClick={() => navigate("/scan")}
              >
                Add Firewall
              </button>
            </div>
          )}
        </div>

        {selected && (
          <div className="firewall-modal">
            <div className="modal-content">
              <div className="modal-header">
                <h3>Firewall Details</h3>
                <button 
                  className="close-modal"
                  onClick={() => setSelected(null)}
                >
                  ×
                </button>
              </div>
              <div className="modal-body">
                <table>
                  <tbody>
                    {Object.entries(selected).map(([k, v]) => (
                      <tr key={k}>
                        <td className="detail-key">{k}</td>
                        <td className="detail-value">{v}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Inventory;