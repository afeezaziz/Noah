import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface StrategyInfo {
  name: string;
  author: string;
  description: string;
  parameters: Record<string, any>;
  is_active: boolean;
}

interface StrategyConfig {
  [key: string]: any;
}

// Add index signature to request interfaces
interface LoadStrategyRequest {
  file_path: string;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

interface ActivateStrategyRequest {
  strategy_name: string;
  parameters: StrategyConfig;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

interface DeactivateStrategyRequest {
  strategy_name: string;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

interface LoadStrategyResponse {
  success: boolean;
  strategy_name: string;
  message?: string; // Optional message field for error details
}

interface ActivateStrategyResponse {
  success: boolean;
  message: string;
}

function StrategyMarketplace() {
  const [strategies, setStrategies] = useState<StrategyInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStrategy, setSelectedStrategy] = useState<StrategyInfo | null>(null);
  const [strategyConfig, setStrategyConfig] = useState<StrategyConfig>({});
  const [file_path, setFilePath] = useState('');

  useEffect(() => {
    fetchStrategies();
  }, []);

  const fetchStrategies = async () => {
    try {
      setLoading(true);
      const data: StrategyInfo[] = await invoke('get_strategies');
      setStrategies(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching strategies:', err);
      setError('Failed to fetch strategies');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadStrategy = async () => {
    if (!file_path) {
      setError('Please enter a file path');
      return;
    }

    try {
      const response: LoadStrategyResponse = await invoke('load_strategy', { file_path } as LoadStrategyRequest);
      if (response.success) {
        fetchStrategies();
        setFilePath('');
        setError(null);
      } else {
        setError(`Failed to load strategy: ${response.message}`);
      }
    } catch (err) {
      console.error('Error loading strategy:', err);
      setError(`Failed to load strategy: ${err}`);
    }
  };

  const handleActivateStrategy = async (strategyName: string) => {
    try {
      const response: ActivateStrategyResponse = await invoke('activate_strategy', {
        strategy_name: strategyName,
        parameters: strategyConfig
      } as ActivateStrategyRequest);
      if (response.success) {
        fetchStrategies();
        setSelectedStrategy(null);
        setStrategyConfig({});
        setError(null);
      } else {
        setError(`Failed to activate strategy: ${response.message}`);
      }
    } catch (err) {
      console.error('Error activating strategy:', err);
      setError(`Failed to activate strategy: ${err}`);
    }
  };

  const handleDeactivateStrategy = async (strategyName: string) => {
    try {
      const response: ActivateStrategyResponse = await invoke('deactivate_strategy', {
        strategy_name: strategyName
      } as DeactivateStrategyRequest);
      if (response.success) {
        fetchStrategies();
        setError(null);
      } else {
        setError(`Failed to deactivate strategy: ${response.message}`);
      }
    } catch (err) {
      console.error('Error deactivating strategy:', err);
      setError(`Failed to deactivate strategy: ${err}`);
    }
  };

  const handleParameterChange = (paramName: string, value: any) => {
    setStrategyConfig({
      ...strategyConfig,
      [paramName]: value
    });
  };

  if (loading) {
    return <div className="strategy-marketplace">Loading strategies...</div>;
  }

  if (error) {
    return <div className="strategy-marketplace error">{error}</div>;
  }

  return (
    <div className="strategy-marketplace">
      <h2>Strategy Marketplace</h2>
      
      <div className="load-strategy">
        <h3>Load New Strategy</h3>
        <div className="load-form">
          <input
            type="text"
            value={file_path}
            onChange={(e) => setFilePath(e.target.value)}
            placeholder="Enter path to strategy file"
          />
          <button onClick={handleLoadStrategy}>Load Strategy</button>
        </div>
      </div>
      
      <div className="strategies-list">
        <h3>Available Strategies</h3>
        {strategies.length > 0 ? (
          <div className="strategy-cards">
            {strategies.map((strategy) => (
              <div 
                key={strategy.name} 
                className={`strategy-card ${strategy.is_active ? 'active' : ''}`}
              >
                <h4>{strategy.name}</h4>
                <p className="author">by {strategy.author}</p>
                <p className="description">{strategy.description}</p>
                
                <div className="strategy-actions">
                  {!strategy.is_active ? (
                    <button 
                      onClick={() => setSelectedStrategy(strategy)}
                    >
                      Configure & Activate
                    </button>
                  ) : (
                    <button 
                      onClick={() => handleDeactivateStrategy(strategy.name)}
                      className="deactivate"
                    >
                      Deactivate
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No strategies available. Load a strategy to get started.</p>
        )}
      </div>
      
      {selectedStrategy && (
        <div className="modal">
          <div className="modal-content">
            <span 
              className="close" 
              onClick={() => setSelectedStrategy(null)}
            >
              &times;
            </span>
            <h3>Configure Strategy: {selectedStrategy.name}</h3>
            <p>{selectedStrategy.description}</p>
            
            <div className="strategy-parameters">
              <h4>Parameters</h4>
              {Object.entries(selectedStrategy.parameters).map(([key, value]) => (
                <div key={key} className="parameter">
                  <label htmlFor={key}>{key}:</label>
                  <input
                    type="text"
                    id={key}
                    value={strategyConfig[key] !== undefined ? strategyConfig[key] : value}
                    onChange={(e) => handleParameterChange(key, e.target.value)}
                  />
                </div>
              ))}
            </div>
            
            <button 
              onClick={() => handleActivateStrategy(selectedStrategy.name)}
            >
              Activate Strategy
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default StrategyMarketplace;