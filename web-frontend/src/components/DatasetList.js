import React, { useState, useEffect } from 'react';
import api from '../services/api';

const DatasetList = ({ onDatasetSelect }) => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const response = await api.get('/datasets/');
      setDatasets(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch datasets. Please try again.');
      console.error('Error fetching datasets:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return <div className="loading">Loading datasets...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={fetchDatasets}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dataset-list">
      <h2>Equipment Datasets</h2>
      {datasets.length === 0 ? (
        <div className="empty-state">
          <p>No datasets found. Upload a CSV file to get started.</p>
        </div>
      ) : (
        <div className="datasets-grid">
          {datasets.map((dataset) => (
            <div 
              key={dataset.id} 
              className="dataset-card"
              onClick={() => onDatasetSelect(dataset)}
            >
              <h3>{dataset.name}</h3>
              <div className="dataset-info">
                <p><strong>File:</strong> {dataset.file_name}</p>
                <p><strong>Uploaded:</strong> {formatDate(dataset.upload_date)}</p>
                <p><strong>Equipment Count:</strong> {dataset.equipment_count || dataset.total_count}</p>
              </div>
              <div className="dataset-stats">
                <div className="stat">
                  <span className="label">Avg Flowrate:</span>
                  <span className="value">{dataset.avg_flowrate?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="label">Avg Pressure:</span>
                  <span className="value">{dataset.avg_pressure?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="label">Avg Temperature:</span>
                  <span className="value">{dataset.avg_temperature?.toFixed(2) || 'N/A'}</span>
                </div>
              </div>
              <button className="view-btn">View Details</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DatasetList;
