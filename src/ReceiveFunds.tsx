import React, { useState } from 'react';

function ReceiveFunds() {
  const [address, setAddress] = useState('bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq');
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(address);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="receive-funds">
      <h2>Receive Funds</h2>
      <div className="address-display">
        <p>Your receiving address:</p>
        <div className="address-qr">
          <div className="qr-code-placeholder">
            {/* In a real implementation, this would be an actual QR code */}
            <div className="qr-code">QR CODE</div>
          </div>
          <div className="address-text">
            <p>{address}</p>
            <button onClick={copyToClipboard}>
              {copied ? 'Copied!' : 'Copy Address'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReceiveFunds;