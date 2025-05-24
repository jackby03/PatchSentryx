import React from 'react';
import './sidebar.css';
import { useNavigate } from 'react-router-dom';
import { getFirewalls } from '../../services/services';

const Sidebar = () => {
  const navigate = useNavigate();

  const handleLaunchScan = async () => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      navigate("/");
      return;
    }
    const firewalls = await getFirewalls();
    const userFirewalls = firewalls.filter(fw => fw.collection_id === userId);
    if (userFirewalls.length === 0) {
      navigate("/scan");
    } else {
      navigate("/inventory");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("userId");
    navigate("/");
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>PathSentryx</h1>
        <p>Drink Providers on Promise Developers</p>
      </div>
      
      <div className="sidebar-section">
        <button className="launch-scan-btn" onClick={handleLaunchScan}>Launch Scan</button>
      </div>
      
      <nav className="sidebar-nav">
        <ul>
          <li>
            <a
              href="/dashboard"
              style={{ color: "#fff", textDecoration: "none" }}
              className="sidebar-button"
            >
              Dashboard
            </a>
          </li>
          <li>
            <a
              href="/inventory"
              style={{ color: "#fff", textDecoration: "none" }}
              className="sidebar-button"
            >
              Inventory
            </a>
          </li>
          <li>
            <span style={{ color: "#fff" }}>Compliance</span>
          </li>
          <li>
            <span style={{ color: "#fff" }}>Issues</span>
          </li>
        </ul>
      </nav>
      
      <div className="sidebar-footer">
        <ul>
          <li>
            <span style={{ color: "#fff" }}>Settings</span>
          </li>
          <li>
            <button
              onClick={handleLogout}
              style={{
                background: "none",
                border: "none",
                color: "#fff",
                cursor: "pointer",
                padding: 0,
                textAlign: "left"
              }}
            >
              Log Out
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;