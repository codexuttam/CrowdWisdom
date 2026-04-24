import os
import sys
import json
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from agents.trading_agent import TradingAgent

def main():
    
    # Check for API keys
    if not os.getenv("OPENROUTER_API_KEY"):
        print("WARNING: OPENROUTER_API_KEY not set in .env. Agent might fail.")
    if not os.getenv("APIFY_API_KEY"):
        print("WARNING: APIFY_API_KEY not set in .env. Historical research will be mocked.")

    agent = TradingAgent()
    
    # The Task for the agent
    initial_task = (
        "You are a Senior Crypto Trading Analyst. Your goal is to find the best 5-minute prediction "
        "opportunities for BTC and ETH. \n"
        "Workflow:\n"
        "1. Use 'market_search' to find current markets on PolyMarket and Kalshi.\n"
        "2. For a selected market, use 'research_data' to get the last 1000 bars (5m interval).\n"
        "3. Use 'predict_move' to run the Kronos model on the research data.\n"
        "4. Use 'risk_management' to calculate position sizing based on the prediction and market price.\n"
        "5. Provide a summary of the trade recommendation including the rationale.\n"
        "6. Finally, self-reflect: if the prediction confidence is low or risk is too high, suggest what "
        "extra data would improve the prediction."
    )

    print("--- CrowdWisdom Trading Agent Loop Starting ---")
    
    try:
        result = agent.run(initial_task)
        
        print("\n--- Final Recommendation ---")
        if isinstance(result, dict) and "final_response" in result:
            print(result["final_response"])
        else:
            print(result)
            
        # Optional: Feedback loop - ask the agent to refine or scale
        # scale_task = "Now, think about how to scale this to 10 more assets and implement an arbitrage check between Polymarket and Kalshi."
        # agent.run(scale_task)

    except Exception as e:
        print(f"Error in agent execution: {e}")

if __name__ == "__main__":
    main()
