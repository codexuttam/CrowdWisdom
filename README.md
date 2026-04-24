# CrowdWisdom Trading Agent

An advanced, multi-agent crypto market analysis system built using the **Hermes-Agent** framework. This system leverages the **Kronos AI model** to predict short-term price movements and implements a robust agentic workflow for market search, research, and risk management.

## 🚀 Features

- **Agentic Workflow**: A multi-step autonomous loop (Search → Research → Predict → Risk → Recommend).
- **Kronos Prediction Engine**: Uses a 100M parameter time-series model to forecast 5-minute price trends using 1,000 historical bars.
- **Smart Pipeline**: Self-healing tool logic that auto-fetches data if LLM state management fails during multi-step hand-offs.
- **Robust Data Connectivity**: Triple-layer data acquisition (PolyMarket/Kalshi Search, Apify Scraping, and a Direct Binance Fallback).
- **Kelly Criterion**: Quantitative position sizing based on model confidence and market-implied probabilities.

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd CrowdWisdom
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and add your keys:
   ```bash
   cp .env.example .env
   ```
   Required keys:
   - `OPENROUTER_API_KEY`: For the LLM (Tencent Hy3-Preview).
   - `APIFY_API_KEY`: For historical data scraping.

## 📈 Running the Agent

Run the main execution loop:
```bash
python main.py
```

The agent will automatically:
1. Search for BTC/ETH prediction markets.
2. Retrieve 1,000 bars of 5-minute OHLCV data.
3. Generate a directional price prediction using Kronos.
4. Provide a risk-managed trade recommendation summary.

## 🏗️ Technical Architecture

- **Framework**: [Hermes-Agent](https://github.com/NousResearch/hermes-agent)
- **Model**: [Kronos](https://github.com/shiyu-coder/Kronos)
- **LLM**: Tencent Hy3-Preview (via OpenRouter)
- **Data Source**: Binance, PolyMarket, Kalshi, Apify

---
*Created as part of an AI/Python Internship Assessment.*
