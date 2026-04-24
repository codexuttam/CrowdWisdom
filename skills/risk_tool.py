import json
from typing import Dict, Any

def calculate_kelly(prob_win: float, odds: float, bankroll_fraction: float = 1.0) -> Dict[str, Any]:
    """
    Calculates the Kelly Criterion fraction.
    f* = (p(b+1) - 1) / b
    where:
    p = probability of win
    b = net odds (odds - 1, or profit/stake)
    """
    if odds <= 0:
        return {"error": "Odds must be greater than 0"}
    
    # Net odds
    b = odds
    p = prob_win
    q = 1 - p
    
    # Kelly formula
    kelly_f = (p * (b + 1) - 1) / b
    
    # Recommended bet
    recommended_fraction = max(0, kelly_f) * bankroll_fraction
    
    return {
        "kelly_fraction": kelly_f,
        "recommended_fraction": recommended_fraction,
        "is_positive": kelly_f > 0
    }

def risk_tool_handler(args: Dict[str, Any], **kwargs) -> str:
    prob_win = args.get("win_probability", 0.5)
    market_price = args.get("market_price", 0.5) # For PolyMarket, price is between 0 and 1
    
    # In PolyMarket, if price is P, and it pays 1, the net odds b = (1-P)/P
    if market_price <= 0 or market_price >= 1:
        return json.dumps({"error": "Market price must be between 0 and 1 (exclusive)"})
    
    b = (1.0 - market_price) / market_price
    
    res = calculate_kelly(prob_win, b)
    res["win_probability"] = prob_win
    res["market_price"] = market_price
    
    return json.dumps(res, indent=2)

RISK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "risk_management",
        "description": "Calculate the recommended position size based on Kelly Criterion.",
        "parameters": {
            "type": "object",
            "properties": {
                "win_probability": {
                    "type": "number",
                    "description": "Predicted probability of winning (0 to 1)."
                },
                "market_price": {
                    "type": "number",
                    "description": "Current market price for the 'Yes' outcome (0 to 1)."
                }
            },
            "required": ["win_probability", "market_price"]
        }
    }
}

if __name__ == "__main__":
    # Test
    print(risk_tool_handler({"win_probability": 0.6, "market_price": 0.5}))
