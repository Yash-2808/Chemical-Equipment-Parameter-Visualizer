import React, { useState, useEffect } from 'react';
import './App.css';
import DatasetList from './components/DatasetList';
import DatasetDetail from './components/DatasetDetail';
import CSVUpload from './components/CSVUpload';
import Analytics from './components/Analytics';
import Login from './components/Login';
import api from './services/api';

function App() {
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [activeView, setActiveView] = useState('list');
  const [analytics, setAnalytics] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for existing API key in localStorage
    const savedApiKey = localStorage.getItem('apiKey');
    if (savedApiKey) {
      setIsAuthenticated(true);
      updateApiHeaders(savedApiKey);
      fetchAnalytics();
    }
  }, []);

  const updateApiHeaders = (key) => {
    api.defaults.headers.common['X-API-Key'] = key;
  };

  const handleLogin = (key) => {
    setIsAuthenticated(true);
    updateApiHeaders(key);
    fetchAnalytics();
  };

  const handleLogout = () => {
    localStorage.removeItem('apiKey');
    setIsAuthenticated(false);
    delete api.defaults.headers.common['X-API-Key'];
    setSelectedDataset(null);
    setActiveView('list');
    setAnalytics(null);
  };

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
      {!isAuthenticated ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
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
          <button 
            className="logout-button"
            onClick={handleLogout}
          >
            🚪 Logout
          </button>
        </nav>
      </header>
      <main className="App-main">
        {renderContent()}
      </main>
        </>
      )}
    </div>
  );
}

export default App;
