import sqlite3
from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
from base_strategy import BaseStrategy

class Backtester:
    """Backtesting engine for trading strategies."""
    
    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path
        
    def fetch_historical_data(self, symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Fetch historical market data from the database.
        
        Args:
            symbol: Trading symbol
            start_date: Start date for data retrieval
            end_date: End date for data retrieval
            
        Returns:
            DataFrame with historical market data
        """
        conn = sqlite3.connect(self.db_path)
        
        # In a real implementation, you would fetch actual historical data
        # For now, we'll generate simulated data
        dates = pd.date_range(start=start_date, end=end_date, freq='1min')
        prices = [65000 + i * 0.1 for i in range(len(dates))]
        
        data = pd.DataFrame({
            'timestamp': dates,
            'symbol': symbol,
            'open': prices,
            'high': [p + 100 for p in prices],
            'low': [p - 100 for p in prices],
            'close': [p + 50 for p in prices],
            'volume': [1000000 + i * 1000 for i in range(len(dates))]
        })
        
        conn.close()
        return data
    
    def run_backtest(self, strategy: BaseStrategy, symbol: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Run a backtest for a given strategy.
        
        Args:
            strategy: Strategy to backtest
            symbol: Trading symbol
            start_date: Start date for backtest
            end_date: End date for backtest
            
        Returns:
            Dictionary with backtest results
        """
        # Fetch historical data
        data = self.fetch_historical_data(symbol, start_date, end_date)
        
        # Initialize tracking variables
        portfolio_value = 100000.0  # Starting portfolio value
        positions = {}  # Current positions
        trades = []  # Trade history
        portfolio_history = []  # Portfolio value history
        
        # Run the backtest
        for index, row in data.iterrows():
            # Create market data dictionary
            market_data = {
                'symbol': row['symbol'],
                'price': row['close'],
                'timestamp': row['timestamp'].isoformat(),
                'sma_short': row['close'] - 100,  # Simulated short SMA
                'sma_long': row['close'] - 200   # Simulated long SMA
            }
            
            # Get signals from strategy
            signals = strategy.on_tick(market_data)
            
            # Process signals
            for signal in signals:
                if signal['action'] == 'BUY':
                    # Simulate buying
                    amount = signal['amount']
                    price = row['close']
                    cost = amount * price
                    
                    if portfolio_value >= cost:
                        portfolio_value -= cost
                        positions[symbol] = positions.get(symbol, 0) + amount
                        trades.append({
                            'timestamp': row['timestamp'].isoformat(),
                            'action': 'BUY',
                            'symbol': symbol,
                            'amount': amount,
                            'price': price,
                            'cost': cost
                        })
                elif signal['action'] == 'SELL':
                    # Simulate selling
                    if symbol in positions and positions[symbol] > 0:
                        amount = min(signal['amount'], positions[symbol])
                        price = row['close']
                        revenue = amount * price
                        
                        portfolio_value += revenue
                        positions[symbol] -= amount
                        trades.append({
                            'timestamp': row['timestamp'].isoformat(),
                            'action': 'SELL',
                            'symbol': symbol,
                            'amount': amount,
                            'price': price,
                            'revenue': revenue
                        })
            
            # Calculate current portfolio value
            current_positions_value = sum(positions.get(sym, 0) * row['close'] for sym in positions)
            total_value = portfolio_value + current_positions_value
            portfolio_history.append({
                'timestamp': row['timestamp'].isoformat(),
                'portfolio_value': total_value,
                'cash': portfolio_value,
                'positions_value': current_positions_value
            })
        
        # Calculate performance metrics
        initial_value = 100000.0
        final_value = portfolio_history[-1]['portfolio_value'] if portfolio_history else initial_value
        total_return = (final_value - initial_value) / initial_value
        
        # Calculate max drawdown
        peak = initial_value
        max_drawdown = 0
        for point in portfolio_history:
            if point['portfolio_value'] > peak:
                peak = point['portfolio_value']
            drawdown = (peak - point['portfolio_value']) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Calculate Sharpe ratio (simplified)
        returns = [0]  # Start with 0 return for the first period
        for i in range(1, len(portfolio_history)):
            ret = (portfolio_history[i]['portfolio_value'] - portfolio_history[i-1]['portfolio_value']) / portfolio_history[i-1]['portfolio_value']
            returns.append(ret)
        
        avg_return = sum(returns) / len(returns) if returns else 0
        std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5 if returns else 0
        sharpe_ratio = avg_return / std_dev if std_dev > 0 else 0
        
        return {
            'strategy_name': strategy.name,
            'symbol': symbol,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'initial_value': initial_value,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_percent': f"{total_return * 100:.2f}%",
            'max_drawdown': max_drawdown,
            'max_drawdown_percent': f"{max_drawdown * 100:.2f}%",
            'sharpe_ratio': sharpe_ratio,
            'total_trades': len(trades),
            'trades': trades,
            'portfolio_history': portfolio_history
        }

# Example usage
if __name__ == "__main__":
    from base_strategy import SimpleMAStrategy
    
    # Create backtester
    backtester = Backtester()
    
    # Create strategy
    strategy = SimpleMAStrategy()
    
    # Run backtest
    results = backtester.run_backtest(
        strategy,
        "BTC",
        datetime.now() - timedelta(days=7),
        datetime.now()
    )
    
    # Print results
    print(f"Backtest Results for {results['strategy_name']}")
    print(f"Symbol: {results['symbol']}")
    print(f"Period: {results['start_date']} to {results['end_date']}")
    print(f"Initial Value: ${results['initial_value']:,.2f}")
    print(f"Final Value: ${results['final_value']:,.2f}")
    print(f"Total Return: {results['total_return_percent']}")
    print(f"Max Drawdown: {results['max_drawdown_percent']}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Total Trades: {results['total_trades']}")