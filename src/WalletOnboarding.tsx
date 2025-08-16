import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface GenerateSeedResponse {
  seed_phrase: string;
}

interface DeriveKeyRequest {
  seed_phrase: string;
  path: string;
  [key: string]: unknown; // Index signature to make it compatible with InvokeArgs
}

interface DeriveKeyResponse {
  private_key: string;
}

function WalletOnboarding() {
  const [step, setStep] = useState(1);
  const [seedPhrase, setSeedPhrase] = useState('');
  const [confirmSeedPhrase, setConfirmSeedPhrase] = useState('');
  const [password, setPassword] = useState('');
  const [derivedKey, setDerivedKey] = useState('');

  const handleGenerateSeed = async () => {
    try {
      const result: GenerateSeedResponse = await invoke('generate_new_seed');
      setSeedPhrase(result.seed_phrase);
      setStep(2);
    } catch (error) {
      console.error('Error generating seed:', error);
    }
  };

  const handleConfirmSeed = () => {
    if (seedPhrase === confirmSeedPhrase) {
      setStep(3);
    } else {
      alert('Seed phrases do not match. Please try again.');
    }
  };

  const handleDeriveKey = async () => {
    try {
      const request: DeriveKeyRequest = {
        seed_phrase: seedPhrase,
        path: "m/84'/0'/0'/0/0" // Example derivation path
      };
      const result: DeriveKeyResponse = await invoke('derive_private_key_for_path', request);
      setDerivedKey(result.private_key);
      setStep(4);
    } catch (error) {
      console.error('Error deriving key:', error);
    }
  };

  const handleImportSeed = async () => {
    try {
      await invoke('import_from_seed', { seed_phrase: seedPhrase });
      setStep(4);
    } catch (error) {
      console.error('Error importing seed:', error);
    }
  };

  return (
    <div className="wallet-onboarding">
      <h1>Noah Wallet Setup</h1>
      
      {step === 1 && (
        <div className="step">
          <h2>Create New Wallet</h2>
          <p>Generate a new seed phrase to create your wallet</p>
          <button onClick={handleGenerateSeed}>Generate New Seed</button>
          
          <div className="import-option">
            <p>Already have a seed phrase?</p>
            <button onClick={() => setStep(5)}>Import Existing Wallet</button>
          </div>
        </div>
      )}
      
      {step === 2 && (
        <div className="step">
          <h2>Backup Your Seed Phrase</h2>
          <p>Please write down these 12 words and store them in a secure location</p>
          <div className="seed-phrase">{seedPhrase}</div>
          <button onClick={() => setStep(3)}>I've Written It Down</button>
        </div>
      )}
      
      {step === 3 && (
        <div className="step">
          <h2>Confirm Your Seed Phrase</h2>
          <p>Please enter your seed phrase to confirm you've backed it up correctly</p>
          <textarea
            value={confirmSeedPhrase}
            onChange={(e) => setConfirmSeedPhrase(e.target.value)}
            placeholder="Enter your seed phrase"
          />
          <button onClick={handleConfirmSeed}>Confirm Seed Phrase</button>
        </div>
      )}
      
      {step === 4 && (
        <div className="step">
          <h2>Set Password</h2>
          <p>Set a password to encrypt your wallet</p>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
          />
          <button onClick={handleDeriveKey}>Set Password and Finish</button>
        </div>
      )}
      
      {step === 5 && (
        <div className="step">
          <h2>Import Existing Wallet</h2>
          <p>Enter your existing seed phrase</p>
          <textarea
            value={seedPhrase}
            onChange={(e) => setSeedPhrase(e.target.value)}
            placeholder="Enter your seed phrase"
          />
          <button onClick={handleImportSeed}>Import Wallet</button>
        </div>
      )}
    </div>
  );
}

export default WalletOnboarding;