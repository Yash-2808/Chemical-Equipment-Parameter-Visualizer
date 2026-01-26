import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Analytics = ({ data }) => {
  if (!data) {
    return <div className="loading">Loading analytics...</div>;
  }

  const getOverallTypeDistribution = () => {
    if (!data.overview?.type_distribution) return null;
    
    const labels = Object.keys(data.overview.type_distribution);
    const chartData = Object.values(data.overview.type_distribution);
    
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data: chartData,
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

  const getRecentDatasetsChart = () => {
    if (!data.recent_datasets) return null;
    
    const labels = data.recent_datasets.map(ds => ds.name);
    const equipmentCounts = data.recent_datasets.map(ds => ds.equipment_count);
    
    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data: equipmentCounts,
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    };
  };

  return (
    <div className="analytics">
      <h2>Global Analytics</h2>
      
      <div className="overview-cards">
        <div className="overview-card">
          <h3>Total Datasets</h3>
          <p className="overview-value">{data.overview?.total_datasets || 0}</p>
        </div>
        <div className="overview-card">
          <h3>Total Equipment</h3>
          <p className="overview-value">{data.overview?.total_equipment || 0}</p>
        </div>
        <div className="overview-card">
          <h3>Equipment Types</h3>
          <p className="overview-value">{Object.keys(data.overview?.type_distribution || {}).length}</p>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-container">
          <h3>Overall Equipment Type Distribution</h3>
          {getOverallTypeDistribution() && (
            <div className="chart-wrapper">
              <Pie data={getOverallTypeDistribution()} options={{ responsive: true }} />
            </div>
          )}
        </div>

        <div className="chart-container">
          <h3>Recent Datasets - Equipment Count</h3>
          {getRecentDatasetsChart() && (
            <div className="chart-wrapper">
              <Bar data={getRecentDatasetsChart()} options={{ responsive: true }} />
            </div>
          )}
        </div>
      </div>

      <div className="recent-datasets-section">
        <h3>Recent Datasets</h3>
        {data.recent_datasets?.length > 0 ? (
          <div className="recent-datasets-grid">
            {data.recent_datasets.map((dataset) => (
              <div key={dataset.id} className="recent-dataset-card">
                <h4>{dataset.name}</h4>
                <p><strong>Equipment Count:</strong> {dataset.equipment_count}</p>
                <p><strong>Uploaded:</strong> {new Date(dataset.upload_date).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>No datasets available yet.</p>
        )}
      </div>

      <div className="type-distribution-section">
        <h3>Detailed Type Distribution</h3>
        {data.overview?.type_distribution ? (
          <div className="type-distribution-list">
            {Object.entries(data.overview.type_distribution)
              .sort(([,a], [,b]) => b - a)
              .map(([type, count]) => (
                <div key={type} className="type-item">
                  <span className="type-name">{type}</span>
                  <span className="type-count">{count}</span>
                </div>
              ))}
          </div>
        ) : (
          <p>No equipment type data available.</p>
        )}
      </div>
    </div>
  );
};

export default Analytics;
