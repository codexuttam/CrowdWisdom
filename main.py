import os
import sys
import json
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from agents.trading_agent import TradingAgent
from app_utils.logger import get_logger

logger = get_logger()

def run_analysis(asset):
    logger.info(f"--- Starting Analysis for {asset} ---")
    agent = TradingAgent()
    
    initial_task = (
        f"Analyze {asset} for the best 5-minute prediction opportunities. \n"
        "Workflow:\n"
        "1. Search for prediction markets.\n"
        "2. Fetch 1000 bars of historical data.\n"
        "3. Run Kronos prediction.\n"
        "4. Calculate Kelly position sizing.\n"
        "5. Provide final trade recommendation."
    )

    try:
        result = agent.run(initial_task)
        logger.info(f"Analysis for {asset} completed successfully.")
        
        if isinstance(result, dict) and "final_response" in result:
            print(f"\n--- Recommendation for {asset} ---")
            print(result["final_response"])
        else:
            print(result)
    except Exception as e:
        logger.error(f"Error during {asset} analysis: {e}")

def main():
    # Asset list for scale
    assets = os.getenv("ASSET_LIST", "BTC,ETH,SOL").split(",")
    
    # Check for API keys
    if not os.getenv("OPENROUTER_API_KEY"):
        logger.warning("OPENROUTER_API_KEY not set in .env. Agent might fail.")
    if not os.getenv("APIFY_API_KEY"):
        logger.warning("APIFY_API_KEY not set. Historical research will use fallback/mock.")

    logger.info(f"CrowdWisdom Trading Agent starting for assets: {assets}")
    
    for asset in assets:
        asset = asset.strip()
        run_analysis(asset)
        # Small delay to prevent rate limits at scale
        time.sleep(2)

if __name__ == "__main__":
    main()
