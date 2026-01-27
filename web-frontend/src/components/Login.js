import React, { useState } from 'react';
import api from '../services/api';
import './Login.css';

const Login = ({ onLogin }) => {
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Test the API key by making a request to datasets endpoint
      const testApi = api.create({
        baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey,
        },
      });

      await testApi.get('/datasets/');
      
      // If successful, save the API key and notify parent
      localStorage.setItem('apiKey', apiKey);
      onLogin(apiKey);
      
    } catch (err) {
      setError('Invalid API key. Please check and try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    const demoKey = 'demo-api-key-12345';
    setApiKey(demoKey);
    localStorage.setItem('apiKey', demoKey);
    onLogin(demoKey);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🔬 Chemical Equipment Visualizer</h1>
          <p>Enter your API key to access the application</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="apiKey">API Key</label>
            <input
              type="password"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your API key"
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="button-group">
            <button 
              type="submit" 
              className="login-button"
              disabled={loading || !apiKey}
            >
              {loading ? '🔄 Verifying...' : '🚀 Login'}
            </button>
            
            <button 
              type="button"
              className="demo-button"
              onClick={handleDemoLogin}
            >
              🎮 Use Demo Key
            </button>
          </div>
        </form>

        <div className="login-info">
          <h3>Demo Information</h3>
          <p>For demo purposes, use the API key:</p>
          <code>demo-api-key-12345</code>
          <p>Or click "Use Demo Key" above to get started instantly.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
