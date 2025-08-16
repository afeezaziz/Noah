# Noah User Guide

Welcome to Noah, the autonomous financial agent for Bitcoin DeFi trading. This guide will help you get started with using Noah's features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Wallet Management](#wallet-management)
3. [Market Data](#market-data)
4. [Trading Strategies](#trading-strategies)
5. [AI Assistant](#ai-assistant)

## Getting Started

### Installation

1. Download the latest release for your operating system from the [releases page](https://github.com/afeezaziz/Noah/releases).
2. Install the application following the instructions for your OS:
   - **Windows**: Run the `.exe` installer
   - **macOS**: Drag the `.app` to your Applications folder
   - **Linux**: Run the `.AppImage` file or install the `.deb` package

### First Launch

When you first launch Noah, you'll be guided through the wallet setup process:

1. **Create a New Wallet**: Generate a new BIP39 seed phrase
2. **Backup Your Seed**: Write down and securely store your 12-word seed phrase
3. **Confirm Backup**: Verify your seed phrase by entering it
4. **Set Password**: Create a password to encrypt your wallet

## Wallet Management

### Wallet Dashboard

The dashboard shows your current portfolio value and transaction history.

### Sending Funds

1. Navigate to the "Send" tab
2. Enter the recipient's address
3. Specify the amount to send
4. Review the transaction details
5. Confirm with your password

### Receiving Funds

1. Navigate to the "Receive" tab
2. Share your receiving address or QR code with the sender

## Market Data

Noah continuously ingests market data from various sources:

- Ark L2 state
- Coordinator service fees and queues
- External exchange prices (Binance, Coinbase, etc.)

This data is used for strategy execution and available through the AI assistant.

## Trading Strategies

### Strategy Marketplace

Browse and activate trading strategies:

1. Go to the "Strategies" tab
2. View available strategies
3. Click "Configure & Activate" to set parameters
4. Click "Activate" to start the strategy

### Backtesting

Test strategies with historical data:

1. Go to the "Backtest Studio" tab
2. Select a strategy
3. Set the time period
4. Run the backtest
5. Review performance metrics

### Active Strategies

Monitor your active strategies in the "Strategies" tab. You can deactivate them at any time.

## AI Assistant

### Noah Terminal

Interact with Noah's AI brain:

1. Go to the "Noah Terminal" tab
2. Type natural language questions like:
   - "What is the current BTC price?"
   - "Show me arbitrage opportunities"
   - "What was the funding rate yesterday?"
3. Get instant answers based on real market data

The AI assistant can also help with:
- Strategy analysis and optimization
- Market insights and trends
- Portfolio performance summaries

## Security

Noah prioritizes your security:

- Private keys are never exposed or transmitted
- All transactions require explicit user confirmation
- Wallet data is encrypted with your password
- Market data is stored locally, never transmitted to external servers

## Troubleshooting

### Common Issues

1. **Application won't start**: Ensure you have the latest version installed
2. **Connection errors**: Check your internet connection
3. **Strategy activation fails**: Verify strategy parameters are correct

### Getting Help

For additional support:
- Check the [GitHub issues](https://github.com/afeezaziz/Noah/issues)
- Join our [Discord community](https://discord.gg/example)
- Email support at support@noah.example.com

## Glossary

- **BIP39**: Bitcoin Improvement Proposal 39 - standard for mnemonic seed phrases
- **VTXO**: Virtual eXpireable Transaction Output - Ark L2 transaction format
- **Backtesting**: Testing a strategy against historical data
- **Funding Rate**: Periodic payment between traders in perpetual contracts

---
*Noah - The Autonomous Financial Agent*