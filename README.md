# Noah - The Autonomous Financial Agent

This is a work-in-progress implementation of the Noah project as described in the PRD.md file.

## Current Progress

We have completed the following tasks from the TODO.md file:

1. **Phase 1: Secure Foundation & Core Architecture**
   - [x] 1.1 Initialize the Tauri Project
   - [x] 1.2 Implement the Rust/Python Bridge
   - [x] 1.3 Implement Secure Key Management (Rust Core)
   - [x] 1.4 Create the Signing Oracle (Rust Core)

2. **Phase 2: Data Ingestion & Wallet Functionality**
   - [x] 2.1 Develop the Data Digestion Engine (Python)
   - [x] 2.2 Build the Core Wallet UI (React)
   - [x] 2.3 Implement Wallet State Synchronization

3. **Phase 3: Strategy & Execution Engine**
   - [x] 3.1 Design the `BaseStrategy` API (Python)
   - [x] 3.2 Build the Strategy Marketplace UI (React)
   - [x] 3.3 Develop the Backtesting Engine (Python)
   - [x] 3.4 Develop the Execution Engine (Python)

4. **Phase 4: AI Integration & Final Polish**
   - [x] 4.1 Implement the LLM Brain (Analyst Mode)
   - [x] 4.2 Build the Noah Terminal UI (React)
   - [x] 4.3 Write Comprehensive Documentation

## Project Structure

- `src-tauri`: Rust backend code
  - `key_manager.rs`: Secure key management implementation
  - `lib.rs`: Main Tauri application logic
- `src`: React frontend code
  - `WalletOnboarding.tsx`: Wallet creation/import UI
  - `WalletDashboard.tsx`: Main wallet dashboard
  - `SendFunds.tsx`: Transaction sending UI
  - `ReceiveFunds.tsx`: Fund receiving UI
  - `TransactionSigner.tsx`: Transaction signing UI
  - `StrategyMarketplace.tsx`: Strategy marketplace UI
  - `BacktestStudio.tsx`: Backtesting studio UI
  - `NoahTerminal.tsx`: AI chat interface
- `src-python`: Python engine code
  - `engine.py`: Python REST API server
  - `data_ingestor.py`: Market data ingestion engine
  - `base_strategy.py`: Base strategy API and example implementation
  - `backtester.py`: Backtesting engine
  - `execution_engine.py`: Execution engine
  - `llm_brain.py`: LLM brain with LangChain integration
- `docs`: Documentation
  - `USER_GUIDE.md`: User guide for the application
  - `STRATEGY_DEVELOPER_GUIDE.md`: Guide for strategy developers

## Features Implemented

1. **Tauri + React Setup**: Basic Tauri application with React frontend
2. **Rust/Python Communication**: REST API bridge between Rust and Python
3. **Secure Key Management**:
   - Generate new BIP39 seed phrases
   - Import existing seed phrases
   - Derive private keys from seed phrases
4. **Transaction Signing**:
   - Sign messages with private keys
   - User confirmation dialog for signing
5. **Data Ingestion Engine**:
   - Continuous polling of market data sources
   - SQLite database storage for time-series data
6. **Wallet UI**:
   - Wallet onboarding flow
   - Dashboard with balance and transaction history
   - Send and receive fund functionality
7. **Strategy Engine**:
   - Base strategy API with abstract methods
   - Strategy loading and activation functionality
   - Strategy marketplace UI
   - Backtesting engine with performance metrics
   - Execution engine with risk management
8. **AI Integration**:
   - LLM brain with LangChain integration
   - Natural language querying of market data
   - Chat-like interface (Noah Terminal)
9. **Documentation**:
   - User guide
   - Strategy developer guide

## Next Steps

- Package and release the application

## Getting Started

### Prerequisites

- Rust and Cargo (latest stable)
- Node.js and npm (latest LTS)
- Python 3.8 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/afeezaziz/Noah.git
   cd Noah
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   npm run tauri dev
   ```

## Documentation

- [User Guide](USER_GUIDE.md)
- [Strategy Developer Guide](STRATEGY_DEVELOPER_GUIDE.md)

## Contributing

We welcome contributions to the Noah project! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Noah - The Autonomous Financial Agent*