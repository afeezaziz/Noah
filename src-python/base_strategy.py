from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

class BaseStrategy(ABC):
    """Abstract base class for all trading strategies."""
    
    def __init__(self, name: str, author: str, description: str):
        self.name = name
        self.author = author
        self.description = description
        self.parameters = {}
        self.is_active = False
        
    @abstractmethod
    def on_tick(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Called on each market data tick.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            List of trade signals/actions
        """
        pass
    
    @abstractmethod
    def on_order_fill(self, fill_data: Dict[str, Any]) -> None:
        """
        Called when an order is filled.
        
        Args:
            fill_data: Dictionary containing fill information
        """
        pass
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """Set strategy parameters."""
        self.parameters = parameters
    
    def activate(self) -> None:
        """Activate the strategy."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate the strategy."""
        self.is_active = False

# Example strategy implementation
class SimpleMAStrategy(BaseStrategy):
    """Simple moving average crossover strategy."""
    
    def __init__(self):
        super().__init__(
            name="Simple MA Crossover",
            author="Noah Team",
            description="A simple moving average crossover strategy"
        )
        self.set_parameters({
            "short_window": 50,
            "long_window": 200,
            "capital_allocation": 0.1
        })
    
    def on_tick(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Simple moving average crossover logic.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            List of trade signals
        """
        # This is a simplified implementation
        # In a real strategy, you would implement actual trading logic
        signals = []
        
        # Example signal generation
        if market_data.get("price", 0) > market_data.get("sma_short", 0) and \
           market_data.get("sma_short", 0) > market_data.get("sma_long", 0):
            signals.append({
                "action": "BUY",
                "symbol": market_data.get("symbol", "BTC"),
                "amount": self.parameters.get("capital_allocation", 0.1)
            })
        elif market_data.get("price", 0) < market_data.get("sma_short", 0) and \
             market_data.get("sma_short", 0) < market_data.get("sma_long", 0):
            signals.append({
                "action": "SELL",
                "symbol": market_data.get("symbol", "BTC"),
                "amount": self.parameters.get("capital_allocation", 0.1)
            })
            
        return signals
    
    def on_order_fill(self, fill_data: Dict[str, Any]) -> None:
        """
        Handle order fills.
        
        Args:
            fill_data: Dictionary containing fill information
        """
        # Log the fill or update internal state
        print(f"Order filled: {fill_data}")

# Function to dynamically load strategies
def load_strategy_from_file(file_path: str) -> BaseStrategy:
    """
    Load a strategy from a Python file.
    
    Args:
        file_path: Path to the Python file containing the strategy
        
    Returns:
        Instance of the strategy class
    """
    import importlib.util
    import sys
    
    # Load the module
    spec = importlib.util.spec_from_file_location("strategy_module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["strategy_module"] = module
    spec.loader.exec_module(module)
    
    # Find the strategy class (assuming it's the only class that inherits from BaseStrategy)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, BaseStrategy) and obj != BaseStrategy:
            return obj()
    
    raise ValueError("No valid strategy class found in the file")

# Example usage
if __name__ == "__main__":
    # Create and test the example strategy
    strategy = SimpleMAStrategy()
    print(f"Strategy: {strategy.name}")
    print(f"Author: {strategy.author}")
    print(f"Description: {strategy.description}")
    print(f"Parameters: {strategy.parameters}")
    
    # Simulate market data
    market_data = {
        "symbol": "BTC",
        "price": 65000,
        "sma_short": 64000,
        "sma_long": 63000
    }
    
    # Generate signals
    signals = strategy.on_tick(market_data)
    print(f"Generated signals: {signals}")