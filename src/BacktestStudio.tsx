import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface BacktestResult {
  strategy_name: string;
  symbol: string;
  start_date: string;
  end_date: string;
  initial_value: number;
  final_value: number;
  total_return: number;
  total_return_percent: string;
  max_drawdown: number;
  max_drawdown_percent: string;
  sharpe_ratio: number;
  total_trades: number;
}

interface BacktestResponse {
  success: boolean;
  results: BacktestResult | null;
  message?: string; // Optional message field for error details
}

// Add index signature to request interfaces
interface BacktestRequest {
  strategy_name: string;
  symbol: string;
  start_date: string;
  end_date: string;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

function BacktestStudio() {
  const [strategyName, setStrategyName] = useState('Simple MA Crossover');
  const [symbol, setSymbol] = useState('BTC');
  const [startDate, setStartDate] = useState('2023-01-01T00:00');
  const [endDate, setEndDate] = useState('2023-01-07T00:00');
  const [backtestResult, setBacktestResult] = useState<BacktestResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRunBacktest = async () => {
    setLoading(true);
    setError(null);
    setBacktestResult(null);

    try {
      const response: BacktestResponse = await invoke('run_backtest', {
        strategy_name: strategyName,
        symbol: symbol,
        start_date: new Date(startDate).toISOString(),
        end_date: new Date(endDate).toISOString()
      } as BacktestRequest);

      if (response.success && response.results) {
        setBacktestResult(response.results);
      } else {
        setError('Backtest failed to run');
      }
    } catch (err) {
      console.error('Error running backtest:', err);
      setError(`Failed to run backtest: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="backtest-studio">
      <h2>Strategy Backtesting Studio</h2>
      
      <div className="backtest-form">
        <h3>Configure Backtest</h3>
        <div className="form-group">
          <label htmlFor="strategy">Strategy:</label>
          <input
            type="text"
            id="strategy"
            value={strategyName}
            onChange={(e) => setStrategyName(e.target.value)}
            placeholder="Enter strategy name"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="symbol">Symbol:</label>
          <input
            type="text"
            id="symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="Enter trading symbol"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="start-date">Start Date:</label>
          <input
            type="datetime-local"
            id="start-date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="end-date">End Date:</label>
          <input
            type="datetime-local"
            id="end-date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
        
        <button 
          onClick={handleRunBacktest} 
          disabled={loading}
        >
          {loading ? 'Running Backtest...' : 'Run Backtest'}
        </button>
      </div>
      
      {error && (
        <div className="error">{error}</div>
      )}
      
      {backtestResult && (
        <div className="backtest-results">
          <h3>Backtest Results</h3>
          <div className="results-grid">
            <div className="result-card">
              <h4>Strategy</h4>
              <p>{backtestResult.strategy_name}</p>
            </div>
            <div className="result-card">
              <h4>Symbol</h4>
              <p>{backtestResult.symbol}</p>
            </div>
            <div className="result-card">
              <h4>Period</h4>
              <p>{new Date(backtestResult.start_date).toLocaleDateString()} to {new Date(backtestResult.end_date).toLocaleDateString()}</p>
            </div>
            <div className="result-card">
              <h4>Initial Value</h4>
              <p>${backtestResult.initial_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
            <div className="result-card">
              <h4>Final Value</h4>
              <p>${backtestResult.final_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
            <div className="result-card">
              <h4>Total Return</h4>
              <p className={backtestResult.total_return >= 0 ? 'positive' : 'negative'}>
                {backtestResult.total_return_percent}
              </p>
            </div>
            <div className="result-card">
              <h4>Max Drawdown</h4>
              <p className="negative">{backtestResult.max_drawdown_percent}</p>
            </div>
            <div className="result-card">
              <h4>Sharpe Ratio</h4>
              <p>{backtestResult.sharpe_ratio.toFixed(2)}</p>
            </div>
            <div className="result-card">
              <h4>Total Trades</h4>
              <p>{backtestResult.total_trades}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BacktestStudio;