import React, { useState } from 'react';
import api from '../services/api';

const CSVUpload = ({ onSuccess }) => {
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== 'text/csv' && !selectedFile.name.endsWith('.csv')) {
        setError('Please select a CSV file.');
        return;
      }
      setFile(selectedFile);
      setError(null);
      if (!datasetName) {
        setDatasetName(selectedFile.name.replace('.csv', ''));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    if (datasetName) {
      formData.append('dataset_name', datasetName);
    }

    setUploading(true);
    setError(null);

    try {
      await api.post('/datasets/upload_csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(true);
      setFile(null);
      setDatasetName('');
      
      // Reset form after 2 seconds and call success callback
      setTimeout(() => {
        setSuccess(false);
        onSuccess();
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="csv-upload">
      <h2>Upload CSV File</h2>
      
      {success ? (
        <div className="success-message">
          <h3>✓ Upload Successful!</h3>
          <p>Your dataset has been processed and is ready to view.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="form-group">
            <label htmlFor="file">CSV File:</label>
            <input
              type="file"
              id="file"
              accept=".csv"
              onChange={handleFileChange}
              disabled={uploading}
            />
            <small>
              Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="datasetName">Dataset Name (optional):</label>
            <input
              type="text"
              id="datasetName"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              placeholder="Enter a name for this dataset"
              disabled={uploading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="submit" 
            className="upload-btn"
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload CSV'}
          </button>
        </form>
      )}

      <div className="sample-format">
        <h3>Expected CSV Format:</h3>
        <pre>{`Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,150.5,2.3,75.2
Heat Exchanger B,Heat Exchanger,89.3,1.8,120.5
Valve C,Valve,45.7,3.1,85.3`}</pre>
      </div>
    </div>
  );
};

export default CSVUpload;
