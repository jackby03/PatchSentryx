import React from 'react';
import './dashboard.css';
import Sidebar from '../../sidebar/sidebar';

const Dashboard = () => {
  return (
    <div className="scan-container">
      <Sidebar />
      <div className="scan-content">
        <h2>Dashboard Overview</h2>
        
        <div className="provider-selector">
          <h3>Provider</h3>
          <select>
            <option>Select a provider</option>
            {}
          </select>
        </div>
        
        <div className="providers-overview">
          <h3>PROVIDERS OVERVIEW</h3>
          <div className="overview-table">
            <div className="overview-row">
              <span>Provider</span>
              <span>Percent Passing</span>
              <span>Failing Checks</span>
              <span>Total Resources</span>
            </div>
            <div className="overview-row data">
              <span>AWS</span>
              <span>75.74%</span>
              <span>681</span>
              <span>779</span>
            </div>
          </div>
        </div>
        
        <div className="severity-breakdown">
          <h3>PROBLEMS BY SEVERITY</h3>
          <div className="severity-levels">
            <div className="severity-level">
              <span className="severity-label">Critical</span>
              <span className="severity-percent">47.37%</span>
              <span className="severity-count">40</span>
              <span className="severity-total">44</span>
            </div>
            {/* Other severity levels would follow the same pattern */}
          </div>
        </div>
        
        <button className="add-provider-btn">Add Provider</button>
        
        <div className="latest-findings">
          <h3>LATEST FAILING FINDINGS TO DATE BY SEVERITY</h3>
          <div className="findings-table">
            <div className="findings-header">
              <span>Details</span>
              <span>Finding</span>
              <span>Severity</span>
              <span>Status</span>
              <span>Last seen</span>
              <span>Region</span>
              <span>Service</span>
              <span>Cloud provider</span>
            </div>
            {/* Findings rows would be populated dynamically */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;