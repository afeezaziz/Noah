from typing import Dict, Any, List
from base_strategy import BaseStrategy
import uuid

class ExecutionEngine:
    """Execution engine for trading strategies."""
    
    def __init__(self):
        self.active_strategies = {}
        self.risk_limits = {
            "max_position_size": 0.1,  # 10% of portfolio
            "max_daily_loss": 0.02,    # 2% daily loss limit
            "max_trades_per_hour": 10  # Max 10 trades per hour
        }
        self.daily_losses = 0.0
        self.trades_this_hour = 0
        
    def set_risk_limits(self, limits: Dict[str, Any]) -> None:
        """Set risk limits for the execution engine."""
        self.risk_limits.update(limits)
    
    def register_strategy(self, strategy: BaseStrategy) -> None:
        """Register an active strategy with the execution engine."""
        self.active_strategies[strategy.name] = strategy
    
    def unregister_strategy(self, strategy_name: str) -> None:
        """Unregister a strategy from the execution engine."""
        if strategy_name in self.active_strategies:
            del self.active_strategies[strategy_name]
    
    def check_risk_limits(self, signal: Dict[str, Any]) -> bool:
        """
        Check if a trade signal complies with risk limits.
        
        Args:
            signal: Trade signal from a strategy
            
        Returns:
            True if the signal complies with risk limits, False otherwise
        """
        # Check position size limit
        if signal.get("amount", 0) > self.risk_limits["max_position_size"]:
            print(f"Trade rejected: Position size exceeds limit")
            return False
        
        # Check daily loss limit
        if self.daily_losses >= self.risk_limits["max_daily_loss"]:
            print(f"Trade rejected: Daily loss limit exceeded")
            return False
        
        # Check trades per hour limit
        if self.trades_this_hour >= self.risk_limits["max_trades_per_hour"]:
            print(f"Trade rejected: Hourly trade limit exceeded")
            return False
        
        return True
    
    def construct_ark_intent(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construct an Ark intent from a trade signal.
        
        Args:
            signal: Trade signal from a strategy
            
        Returns:
            Ark intent dictionary
        """
        intent = {
            "id": str(uuid.uuid4()),
            "timestamp": "2023-01-01T00:00:00Z",  # In a real implementation, this would be the current timestamp
            "action": signal["action"].lower(),
            "symbol": signal["symbol"],
            "amount": signal["amount"],
            "metadata": {
                "strategy": signal.get("strategy", "unknown"),
                "version": "1.0"
            }
        }
        
        return intent
    
    def request_signature(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request a signature from the Rust core for an intent.
        
        Args:
            intent: Ark intent to sign
            
        Returns:
            Signed intent dictionary
        """
        # In a real implementation, this would communicate with the Rust core
        # For now, we'll simulate the signing process
        signed_intent = intent.copy()
        signed_intent["signature"] = "simulated_signature"
        signed_intent["public_key"] = "simulated_public_key"
        
        return signed_intent
    
    def submit_intent(self, signed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a signed intent to the Matchmaker/Gateway.
        
        Args:
            signed_intent: Signed Ark intent
            
        Returns:
            Submission result
        """
        # In a real implementation, this would submit to the Matchmaker/Gateway
        # For now, we'll simulate the submission process
        result = {
            "success": True,
            "intent_id": signed_intent["id"],
            "submission_id": str(uuid.uuid4()),
            "message": "Intent submitted successfully"
        }
        
        return result
    
    def execute_signal(self, strategy_name: str, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a trade signal from a strategy.
        
        Args:
            strategy_name: Name of the strategy that generated the signal
            signal: Trade signal from the strategy
            
        Returns:
            Execution result
        """
        # Check if the strategy is active
        if strategy_name not in self.active_strategies:
            return {
                "success": False,
                "message": f"Strategy '{strategy_name}' is not active"
            }
        
        # Check risk limits
        if not self.check_risk_limits(signal):
            return {
                "success": False,
                "message": "Trade rejected due to risk limits"
            }
        
        # Construct Ark intent
        intent = self.construct_ark_intent(signal)
        intent["strategy"] = strategy_name
        
        # Request signature from Rust core
        try:
            signed_intent = self.request_signature(intent)
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to request signature: {str(e)}"
            }
        
        # Submit intent to Matchmaker/Gateway
        try:
            result = self.submit_intent(signed_intent)
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to submit intent: {str(e)}"
            }
        
        # Update trade counters
        self.trades_this_hour += 1
        
        # Update daily losses if this was a sell
        if signal["action"] == "SELL":
            self.daily_losses += 0.001  # Simulated loss
        
        return result
    
    def process_strategy_signals(self) -> List[Dict[str, Any]]:
        """
        Process signals from all active strategies.
        
        Returns:
            List of execution results
        """
        results = []
        
        # Process signals from each active strategy
        for strategy_name, strategy in self.active_strategies.items():
            # In a real implementation, you would get market data from the data ingestion engine
            # For now, we'll simulate market data
            market_data = {
                "symbol": "BTC",
                "price": 65000,
                "timestamp": "2023-01-01T00:00:00Z",
                "sma_short": 64000,
                "sma_long": 63000
            }
            
            # Get signals from the strategy
            signals = strategy.on_tick(market_data)
            
            # Execute each signal
            for signal in signals:
                signal["strategy"] = strategy_name
                result = self.execute_signal(strategy_name, signal)
                results.append(result)
        
        return results

# Example usage
if __name__ == "__main__":
    from base_strategy import SimpleMAStrategy
    
    # Create execution engine
    executor = ExecutionEngine()
    
    # Create and register strategy
    strategy = SimpleMAStrategy()
    strategy.activate()
    executor.register_strategy(strategy)
    
    # Process strategy signals
    results = executor.process_strategy_signals()
    
    # Print results
    for result in results:
        print(f"Execution result: {result}")