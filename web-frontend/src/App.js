import React, { useState, useEffect } from 'react';
import './styles/App.css';
import DatasetList from './components/DatasetList';
import DatasetDetail from './components/DatasetDetail';
import CSVUpload from './components/CSVUpload';
import Analytics from './components/Analytics';
import api from './services/api';

function App() {
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [activeView, setActiveView] = useState('list');
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await api.get('/analytics/');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const handleDatasetSelect = (dataset) => {
    setSelectedDataset(dataset);
    setActiveView('detail');
  };

  const handleUploadSuccess = () => {
    setActiveView('list');
    fetchAnalytics();
  };

  const renderContent = () => {
    switch (activeView) {
      case 'list':
        return <DatasetList onDatasetSelect={handleDatasetSelect} />;
      case 'detail':
        return (
          <DatasetDetail 
            dataset={selectedDataset} 
            onBack={() => setActiveView('list')}
          />
        );
      case 'upload':
        return <CSVUpload onSuccess={handleUploadSuccess} />;
      case 'analytics':
        return <Analytics data={analytics} />;
      default:
        return <DatasetList onDatasetSelect={handleDatasetSelect} />;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <nav className="nav-menu">
          <button 
            className={activeView === 'list' ? 'active' : ''}
            onClick={() => setActiveView('list')}
          >
            Datasets
          </button>
              <button 
                className={activeView === 'upload' ? 'active' : ''}
                onClick={() => setActiveView('upload')}
              >
                Upload CSV
              </button>
          <button 
            className={activeView === 'analytics' ? 'active' : ''}
            onClick={() => setActiveView('analytics')}
          >
            Analytics
          </button>
        </nav>
      </header>
      <main className="App-main">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
