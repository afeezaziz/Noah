import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface SignTransactionRequest {
  seed_phrase: string;
  path: string;
  message: string;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

interface SignTransactionResponse {
  signature: string;
}

function TransactionSigner() {
  const [seedPhrase, setSeedPhrase] = useState('');
  const [derivationPath, setDerivationPath] = useState("m/84'/0'/0'/0/0");
  const [message, setMessage] = useState('');
  const [signature, setSignature] = useState('');

  const handleSignTransaction = async () => {
    try {
      const request: SignTransactionRequest = {
        seed_phrase: seedPhrase,
        path: derivationPath,
        message: message
      };
      const result: SignTransactionResponse = await invoke('sign_transaction', request);
      setSignature(result.signature);
    } catch (error) {
      console.error('Error signing transaction:', error);
      setSignature(`Error: ${error}`);
    }
  };

  return (
    <div className="transaction-signer">
      <h2>Transaction Signer</h2>
      <div>
        <label>Seed Phrase:</label>
        <textarea
          value={seedPhrase}
          onChange={(e) => setSeedPhrase(e.target.value)}
          placeholder="Enter your seed phrase"
        />
      </div>
      <div>
        <label>Derivation Path:</label>
        <input
          type="text"
          value={derivationPath}
          onChange={(e) => setDerivationPath(e.target.value)}
          placeholder="Enter derivation path"
        />
      </div>
      <div>
        <label>Message to Sign:</label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter message to sign"
        />
      </div>
      <button onClick={handleSignTransaction}>Sign Transaction</button>
      {signature && (
        <div>
          <h3>Signature:</h3>
          <p>{signature}</p>
        </div>
      )}
    </div>
  );
}

export default TransactionSigner;