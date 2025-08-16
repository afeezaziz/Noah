from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import sqlite3
from typing import Dict, Any, List
import os

class LLMBrain:
    \"\"\"LLM Brain for the Noah agent.\"\"\"
    
    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path
        self.llm = None
        self.agent_executor = None
        self._initialize_llm()
        
    def _initialize_llm(self):
        \"\"\"Initialize the LLM with OpenAI API.\"\"\"
        # Check if OpenAI API key is set
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set. Using a mock LLM for demonstration.")
            # For demonstration purposes, we'll use a mock LLM
            from langchain_core.language_models import FakeListLLM
            self.llm = FakeListLLM(responses=[
                "I've analyzed the market data and found that BTC price is $65,000 with a 24h change of +2.5%.",
                "Based on the data, I recommend monitoring the BTC/USD pair for potential breakout opportunities.",
                "The current funding rate for BTC is 0.01% which is relatively neutral.",
                "I've identified an arbitrage opportunity between Exchange A and Exchange B with a 0.3% profit margin."
            ])
        else:
            # Initialize OpenAI LLM
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=api_key
            )
        
        # Create tools
        tools = [self.get_price_data, self.get_funding_rates, self.get_arbitrage_opportunities]
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are Noah, an AI-powered financial assistant for Bitcoin DeFi trading. "
                      "You have access to market data tools that you can use to answer questions and provide insights. "
                      "Always be helpful, accurate, and concise in your responses."),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
    @tool
    def get_price_data(self, symbol: str = "BTC") -> Dict[str, Any]:
        \"\"\"
        Get current price data for a symbol.
        
        Args:
            symbol: Trading symbol (default: BTC)
            
        Returns:
            Dictionary with price data
        \"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # In a real implementation, you would fetch actual data from the database
        # For now, we'll return simulated data
        data = {
            "symbol": symbol,
            "price": 65000.0,
            "change_24h": 2.5,
            "volume_24h": 15000000000,
            "high_24h": 66000.0,
            "low_24h": 64000.0
        }
        
        conn.close()
        return data
    
    @tool
    def get_funding_rates(self, symbol: str = "BTC") -> Dict[str, Any]:
        \"\"\"
        Get funding rates for a symbol.
        
        Args:
            symbol: Trading symbol (default: BTC)
            
        Returns:
            Dictionary with funding rate data
        \"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # In a real implementation, you would fetch actual data from the database
        # For now, we'll return simulated data
        data = {
            "symbol": symbol,
            "funding_rate": 0.0001,  # 0.01%
            "next_funding_time": "2023-01-01T08:00:00Z",
            "predicted_rate": 0.00005  # 0.005%
        }
        
        conn.close()
        return data
    
    @tool
    def get_arbitrage_opportunities(self, min_spread: float = 0.1) -> List[Dict[str, Any]]:
        \"\"\"
        Get arbitrage opportunities between exchanges.
        
        Args:
            min_spread: Minimum spread percentage to consider (default: 0.1%)
            
        Returns:
            List of arbitrage opportunities
        \"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # In a real implementation, you would fetch actual data from the database
        # For now, we'll return simulated data
        opportunities = [
            {
                "symbol": "BTC",
                "buy_exchange": "Exchange A",
                "sell_exchange": "Exchange B",
                "buy_price": 64900.0,
                "sell_price": 65100.0,
                "spread": 0.31,  # Percentage
                "potential_profit": 200.0  # In USD
            }
        ]
        
        conn.close()
        return opportunities
    
    def process_query(self, query: str) -> str:
        \"\"\"
        Process a natural language query using the LLM brain.
        
        Args:
            query: Natural language query
            
        Returns:
            Response from the LLM
        \"\"\"
        if not self.agent_executor:
            return "LLM brain not initialized properly."
        
        try:
            result = self.agent_executor.invoke({"input": query})
            return result["output"]
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Create LLM brain
    brain = LLMBrain()
    
    # Process some example queries
    queries = [
        "What is the current price of BTC?",
        "Show me the funding rates for BTC",
        "Are there any arbitrage opportunities with a spread greater than 0.2%?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = brain.process_query(query)
        print(f"Response: {response}\n")