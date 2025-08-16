# src-python/engine.py
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets
import asyncio
import sqlite3
from data_ingestor import DataIngestor
from base_strategy import BaseStrategy, SimpleMAStrategy, load_strategy_from_file
from backtester import Backtester
from execution_engine import ExecutionEngine
from llm_brain import LLMBrain
from typing import List, Dict, Any, Optional

app = FastAPI()

# Generate a secret token for authentication
SECRET_TOKEN = secrets.token_urlsafe(32)
print(f"Secret token: {SECRET_TOKEN}")

# Save the secret token to a file that the Rust backend can read
with open("secret_token.txt", "w") as f:
    f.write(SECRET_TOKEN)

# Initialize the data ingestor
data_ingestor = DataIngestor()

# Initialize the backtester
backtester = Backtester()

# Initialize the execution engine
executor = ExecutionEngine()

# Initialize the LLM brain
llm_brain = LLMBrain()

# Strategy management
strategies = {}
active_strategies = {}

class PingRequest(BaseModel):
    token: str
    message: str

class PingResponse(BaseModel):
    message: str

class WalletDataResponse(BaseModel):
    balance: float
    transactions: List[Dict[str, Any]]

class SendTransactionRequest(BaseModel):
    token: str
    recipient: str
    amount: float

class SendTransactionResponse(BaseModel):
    success: bool
    transaction_id: str

class StrategyInfo(BaseModel):
    name: str
    author: str
    description: str
    parameters: Dict[str, Any]
    is_active: bool

class LoadStrategyRequest(BaseModel):
    token: str
    file_path: str

class LoadStrategyResponse(BaseModel):
    success: bool
    strategy_name: str

class ActivateStrategyRequest(BaseModel):
    token: str
    strategy_name: str
    parameters: Dict[str, Any]

class ActivateStrategyResponse(BaseModel):
    success: bool
    message: str

class BacktestRequest(BaseModel):
    token: str
    strategy_name: str
    symbol: str
    start_date: str
    end_date: str

class BacktestResponse(BaseModel):
    success: bool
    results: Optional[Dict[str, Any]]

class ExecuteSignalRequest(BaseModel):
    token: str
    strategy_name: str
    signal: Dict[str, Any]

class ExecuteSignalResponse(BaseModel):
    success: bool
    message: str
    execution_id: Optional[str]

class LLMQueryRequest(BaseModel):
    token: str
    query: str

class LLMQueryResponse(BaseModel):
    success: bool
    response: str

@app.get("/")
def read_root():
    return {"message": "Noah Python Engine is running"}

@app.post("/ping", response_model=PingResponse)
def ping(request: PingRequest):
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return PingResponse(message=f"pong: {request.message}")

@app.get("/wallet/data", response_model=WalletDataResponse)
def get_wallet_data():
    # In a real implementation, this would fetch data from the Ark MCP Gateway
    # For now, we'll return simulated data
    return WalletDataResponse(
        balance=1.25,
        transactions=[
            {
                "id": "tx1",
                "amount": 0.5,
                "timestamp": "2023-01-01T12:00:00Z",
                "type": "receive"
            },
            {
                "id": "tx2",
                "amount": -0.25,
                "timestamp": "2023-01-02T14:30:00Z",
                "type": "send"
            }
        ]
    )

@app.post("/wallet/send", response_model=SendTransactionResponse)
def send_transaction(request: SendTransactionRequest):
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # In a real implementation, this would construct and send a transaction
    # For now, we'll just simulate the process
    import uuid
    transaction_id = str(uuid.uuid4())
    
    return SendTransactionResponse(
        success=True,
        transaction_id=transaction_id
    )

@app.get("/strategies", response_model=List[StrategyInfo])
def get_strategies():
    """Get information about all loaded strategies."""
    strategy_list = []
    
    # Add the example strategy
    example_strategy = SimpleMAStrategy()
    strategy_list.append(StrategyInfo(
        name=example_strategy.name,
        author=example_strategy.author,
        description=example_strategy.description,
        parameters=example_strategy.parameters,
        is_active=example_strategy.is_active
    ))
    
    # Add other loaded strategies
    for name, strategy in strategies.items():
        strategy_list.append(StrategyInfo(
            name=strategy.name,
            author=strategy.author,
            description=strategy.description,
            parameters=strategy.parameters,
            is_active=strategy.is_active
        ))
    
    return strategy_list

@app.post("/strategies/load", response_model=LoadStrategyResponse)
def load_strategy(request: LoadStrategyRequest):
    """Load a strategy from a file."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        strategy = load_strategy_from_file(request.file_path)
        strategies[strategy.name] = strategy
        return LoadStrategyResponse(
            success=True,
            strategy_name=strategy.name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load strategy: {str(e)}")

@app.post("/strategies/activate", response_model=ActivateStrategyResponse)
def activate_strategy(request: ActivateStrategyRequest):
    """Activate a strategy with specific parameters."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if request.strategy_name not in strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    try:
        strategy = strategies[request.strategy_name]
        strategy.set_parameters(request.parameters)
        strategy.activate()
        active_strategies[request.strategy_name] = strategy
        executor.register_strategy(strategy)
        return ActivateStrategyResponse(
            success=True,
            message=f"Strategy '{request.strategy_name}' activated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to activate strategy: {str(e)}")

@app.post("/strategies/deactivate", response_model=ActivateStrategyResponse)
def deactivate_strategy(request: ActivateStrategyRequest):
    """Deactivate a strategy."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if request.strategy_name not in strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    try:
        strategy = strategies[request.strategy_name]
        strategy.deactivate()
        if request.strategy_name in active_strategies:
            del active_strategies[request.strategy_name]
        executor.unregister_strategy(request.strategy_name)
        return ActivateStrategyResponse(
            success=True,
            message=f"Strategy '{request.strategy_name}' deactivated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to deactivate strategy: {str(e)}")

@app.post("/strategies/backtest", response_model=BacktestResponse)
def run_backtest(request: BacktestRequest):
    """Run a backtest for a strategy."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if request.strategy_name not in strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    try:
        strategy = strategies[request.strategy_name]
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)
        
        results = backtester.run_backtest(strategy, request.symbol, start_date, end_date)
        return BacktestResponse(
            success=True,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to run backtest: {str(e)}")

@app.post("/strategies/execute", response_model=ExecuteSignalResponse)
def execute_signal(request: ExecuteSignalRequest):
    """Execute a trade signal from a strategy."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        result = executor.execute_signal(request.strategy_name, request.signal)
        return ExecuteSignalResponse(
            success=result["success"],
            message=result["message"],
            execution_id=result.get("submission_id")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to execute signal: {str(e)}")

@app.post("/llm/query", response_model=LLMQueryResponse)
def process_llm_query(request: LLMQueryRequest):
    """Process a query with the LLM brain."""
    if request.token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        response = llm_brain.process_query(request.query)
        return LLMQueryResponse(
            success=True,
            response=response
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process LLM query: {str(e)}")

@app.on_event("startup")
async def startup_event():
    # Start the data ingestion in the background
    asyncio.create_task(data_ingestor.ingest_data_continuously())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)