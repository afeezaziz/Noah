import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface SendTransactionResponse {
  success: boolean;
  transaction_id: string;
}

function SendFunds() {
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response: SendTransactionResponse = await invoke(
        'send_transaction',
        {
          recipient,
          amount: parseFloat(amount)
        }
      );
      
      if (response.success) {
        setResult({
          success: true,
          message: `Successfully sent ${amount} BTC to ${recipient}. Transaction ID: ${response.transaction_id}`
        });
        
        // Reset form
        setRecipient('');
        setAmount('');
      } else {
        setResult({
          success: false,
          message: 'Failed to send transaction'
        });
      }
    } catch (error) {
      setResult({
        success: false,
        message: `Error sending transaction: ${error}`
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="send-funds">
      <h2>Send Funds</h2>
      <form onSubmit={handleSend}>
        <div>
          <label htmlFor="recipient">Recipient Address:</label>
          <input
            type="text"
            id="recipient"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
            placeholder="Enter recipient address"
          />
        </div>
        <div>
          <label htmlFor="amount">Amount (BTC):</label>
          <input
            type="number"
            id="amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            min="0"
            step="0.00000001"
            required
            placeholder="Enter amount"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send BTC'}
        </button>
      </form>
      
      {result && (
        <div className={`result ${result.success ? 'success' : 'error'}`}>
          {result.message}
        </div>
      )}
    </div>
  );
}

export default SendFunds;