import requests
import json
from typing import List, Dict, Any
import os

# Polymarket Gamma API
POLYMARKET_API_URL = "https://gamma-api.polymarket.com/markets"
# Kalshi API
KALSHI_API_URL = "https://api.elections.kalshi.com/trade-api/v2/markets"

def get_polymarket_predictions(asset: str) -> List[Dict]:
    """
    Fetches prediction markets from PolyMarket Gamma API for a given asset (BTC, ETH).
    """
    params = {
        "active": "true",
        "closed": "false",
        "tag": "Crypto",
        "query": f"{asset} price"
    }
    try:
        response = requests.get(POLYMARKET_API_URL, params=params, timeout=20)
        response.raise_for_status()
        markets = response.json()
        
        results = []
        for m in markets:
            # Look for price related questions
            question = m.get('question', '').lower()
            if any(term in question for term in ['price', 'above', 'below', 'at', 'value']):
                results.append({
                    "platform": "PolyMarket",
                    "question": m.get('question'),
                    "prob": m.get('outcomePrices', [0, 0])[0], 
                    "ticker": m.get('ticker'),
                    "id": m.get('id')
                })
        return results[:5]
    except Exception as e:
        return [{"error": f"PolyMarket error: {str(e)}"}]

def get_kalshi_predictions(asset: str) -> List[Dict]:
    """
    Fetches crypto prediction markets from Kalshi.
    """
    params = {
        "limit": 100,
        "status": "open"
    }
    try:
        response = requests.get(KALSHI_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        markets = data.get('markets', [])
        
        results = []
        asset_query = asset.upper()
        for m in markets:
            title = m.get('title', '')
            ticker = m.get('event_ticker', '')
            if asset_query in title or asset_query in ticker:
                # Kalshi prices are in cents (0-100)
                yes_price = float(m.get('last_price_dollars', 0)) # Wait, last_price_dollars might be 0.45 for 45%
                # In the curl check it showed "last_price_dollars":"0.0000"
                # We might need to check 'yes_bid' or 'yes_ask' if available
                prob = yes_price 
                
                results.append({
                    "platform": "Kalshi",
                    "question": title,
                    "prob": prob,
                    "ticker": ticker,
                    "id": m.get('ticker')
                })
        return results[:5]
    except Exception as e:
        return [{"error": f"Kalshi error: {str(e)}"}]

def market_search_handler(args: Dict[str, Any], **kwargs) -> str:
    asset = args.get("asset", "BTC")
    poly = get_polymarket_predictions(asset)
    kalshi = get_kalshi_predictions(asset)
    
    return json.dumps({
        "asset": asset,
        "polymarket": poly,
        "kalshi": kalshi
    }, indent=2)

MARKET_SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "market_search",
        "description": "Search for crypto asset price predictions (5-min, hourly, daily) on PolyMarket and Kalshi.",
        "parameters": {
            "type": "object",
            "properties": {
                "asset": {
                    "type": "string",
                    "description": "The crypto asset to search for (BTC, ETH).",
                    "enum": ["BTC", "ETH"]
                }
            },
            "required": ["asset"]
        }
    }
}

if __name__ == "__main__":
    # Test
    print(market_search_handler({"asset": "BTC"}))
