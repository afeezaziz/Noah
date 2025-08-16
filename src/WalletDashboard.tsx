import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface Transaction {
  id: string;
  amount: number;
  timestamp: string;
  type: string;
}

interface WalletData {
  balance: number;
  transactions: Transaction[];
}

function WalletDashboard() {
  const [walletData, setWalletData] = useState<WalletData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWalletData = async () => {
      try {
        setLoading(true);
        const data: WalletData = await invoke('get_wallet_data');
        setWalletData(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching wallet data:', err);
        setError('Failed to fetch wallet data');
      } finally {
        setLoading(false);
      }
    };

    fetchWalletData();
  }, []);

  if (loading) {
    return <div className="wallet-dashboard">Loading wallet data...</div>;
  }

  if (error) {
    return <div className="wallet-dashboard error">{error}</div>;
  }

  if (!walletData) {
    return <div className="wallet-dashboard">No wallet data available</div>;
  }

  return (
    <div className="wallet-dashboard">
      <div className="balance-card">
        <h2>Wallet Balance</h2>
        <p className="balance-amount">{walletData.balance} BTC</p>
      </div>
      
      <div className="transaction-history">
        <h2>Transaction History</h2>
        {walletData.transactions.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Amount</th>
                <th>Type</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {walletData.transactions.map((tx) => (
                <tr key={tx.id}>
                  <td>{tx.id.substring(0, 8)}...</td>
                  <td className={tx.type === 'send' ? 'amount-negative' : 'amount-positive'}>
                    {tx.type === 'send' ? '-' : '+'}{Math.abs(tx.amount)} BTC
                  </td>
                  <td>{tx.type}</td>
                  <td>{new Date(tx.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No transactions found</p>
        )}
      </div>
    </div>
  );
}

export default WalletDashboard;