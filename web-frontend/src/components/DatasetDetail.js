import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import api from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const DatasetDetail = ({ dataset, onBack }) => {
  const [equipment, setEquipment] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (dataset) {
      fetchDatasetData();
    }
  }, [dataset]);

  const fetchDatasetData = async () => {
    try {
      setLoading(true);
      const [equipmentResponse, summaryResponse] = await Promise.all([
        api.get(`/datasets/${dataset.id}/equipment/`),
        api.get(`/datasets/${dataset.id}/summary/`)
      ]);
      
      setEquipment(equipmentResponse.data.results || equipmentResponse.data);
      setSummary(summaryResponse.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dataset details. Please try again.');
      console.error('Error fetching dataset details:', err);
    } finally {
      setLoading(false);
    }
  };

  const getTypeDistributionChart = () => {
    if (!summary?.type_distribution) return null;
    
    const labels = Object.keys(summary.type_distribution);
    const data = Object.values(summary.type_distribution);
    
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data,
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
            '#FF6384',
            '#C9CBCF',
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  const getParameterComparisonChart = () => {
    if (!summary?.statistics) return null;
    
    const stats = summary.statistics;
    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average',
          data: [
            stats.flowrate.avg,
            stats.pressure.avg,
            stats.temperature.avg,
          ],
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
        },
        {
          label: 'Minimum',
          data: [
            stats.flowrate.min,
            stats.pressure.min,
            stats.temperature.min,
          ],
          backgroundColor: 'rgba(255, 99, 132, 0.8)',
        },
        {
          label: 'Maximum',
          data: [
            stats.flowrate.max,
            stats.pressure.max,
            stats.temperature.max,
          ],
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
        },
      ],
    };
  };

  if (loading) {
    return <div className="loading">Loading dataset details...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={fetchDatasetData}>Retry</button>
      </div>
    );
  }

  if (!dataset) {
    return <div className="error">No dataset selected.</div>;
  }

  return (
    <div className="dataset-detail">
      <div className="detail-header">
        <button onClick={onBack} className="back-btn">← Back to Datasets</button>
        <h2>{dataset.name}</h2>
        <p>Uploaded: {new Date(dataset.upload_date).toLocaleString()}</p>
      </div>

      {summary && (
        <div className="summary-section">
          <h3>Summary Statistics</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <h4>Total Equipment</h4>
              <p className="stat-value">{summary.dataset_info.total_count}</p>
            </div>
            <div className="stat-card">
              <h4>Average Flowrate</h4>
              <p className="stat-value">{summary.statistics.flowrate.avg.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h4>Average Pressure</h4>
              <p className="stat-value">{summary.statistics.pressure.avg.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h4>Average Temperature</h4>
              <p className="stat-value">{summary.statistics.temperature.avg.toFixed(2)}</p>
            </div>
          </div>
        </div>
      )}

      <div className="charts-section">
        <div className="chart-container">
          <h3>Equipment Type Distribution</h3>
          {getTypeDistributionChart() && (
            <div className="chart-wrapper">
              <Pie data={getTypeDistributionChart()} options={{ responsive: true }} />
            </div>
          )}
        </div>

        <div className="chart-container">
          <h3>Parameter Comparison</h3>
          {getParameterComparisonChart() && (
            <div className="chart-wrapper">
              <Bar data={getParameterComparisonChart()} options={{ responsive: true }} />
            </div>
          )}
        </div>
      </div>

      <div className="equipment-table-section">
        <h3>Equipment Details</h3>
        <div className="table-wrapper">
          <table className="equipment-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
              </tr>
            </thead>
            <tbody>
              {equipment.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{item.type}</td>
                  <td>{item.flowrate.toFixed(2)}</td>
                  <td>{item.pressure.toFixed(2)}</td>
                  <td>{item.temperature.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DatasetDetail;
