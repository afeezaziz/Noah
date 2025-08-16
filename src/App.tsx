import React, { useState } from 'react';
import WalletOnboarding from './WalletOnboarding';
import WalletDashboard from './WalletDashboard';
import SendFunds from './SendFunds';
import ReceiveFunds from './ReceiveFunds';
import TransactionSigner from './TransactionSigner';
import StrategyMarketplace from './StrategyMarketplace';
import BacktestStudio from './BacktestStudio';
import NoahTerminal from './NoahTerminal';
import './App.css';

function App() {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Noah - The Autonomous Financial Agent</h1>
        
        <nav className="main-nav">
          <button 
            className={currentView === 'dashboard' ? 'active' : ''}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={currentView === 'send' ? 'active' : ''}
            onClick={() => setCurrentView('send')}
          >
            Send
          </button>
          <button 
            className={currentView === 'receive' ? 'active' : ''}
            onClick={() => setCurrentView('receive')}
          >
            Receive
          </button>
          <button 
            className={currentView === 'strategies' ? 'active' : ''}
            onClick={() => setCurrentView('strategies')}
          >
            Strategies
          </button>
          <button 
            className={currentView === 'backtest' ? 'active' : ''}
            onClick={() => setCurrentView('backtest')}
          >
            Backtest Studio
          </button>
          <button 
            className={currentView === 'terminal' ? 'active' : ''}
            onClick={() => setCurrentView('terminal')}
          >
            Noah Terminal
          </button>
          <button 
            className={currentView === 'onboarding' ? 'active' : ''}
            onClick={() => setShowOnboarding(true)}
          >
            Wallet Setup
          </button>
          <button 
            className={currentView === 'signer' ? 'active' : ''}
            onClick={() => setCurrentView('signer')}
          >
            Transaction Signer
          </button>
        </nav>
        
        <div className="content">
          {currentView === 'dashboard' && <WalletDashboard />}
          {currentView === 'send' && <SendFunds />}
          {currentView === 'receive' && <ReceiveFunds />}
          {currentView === 'strategies' && <StrategyMarketplace />}
          {currentView === 'backtest' && <BacktestStudio />}
          {currentView === 'terminal' && <NoahTerminal />}
          {currentView === 'signer' && <TransactionSigner />}
        </div>
        
        {showOnboarding && (
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={() => setShowOnboarding(false)}>&times;</span>
              <WalletOnboarding />
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;