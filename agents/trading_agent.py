import sys
import os
import json
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run_agent import AIAgent
from tools.registry import registry

# Import skills and register them
from skills.market_search import MARKET_SEARCH_SCHEMA, market_search_handler
from skills.research_tool import RESEARCH_TOOL_SCHEMA, research_tool_handler
from skills.prediction_tool import PREDICTION_TOOL_SCHEMA, prediction_tool_handler
from skills.risk_tool import RISK_TOOL_SCHEMA, risk_tool_handler

def register_custom_tools():
    registry.register(
        name="market_search",
        toolset="crowd_wisdom",
        schema=MARKET_SEARCH_SCHEMA,
        handler=lambda args, **kw: market_search_handler(args, **kw)
    )
    registry.register(
        name="research_data",
        toolset="crowd_wisdom",
        schema=RESEARCH_TOOL_SCHEMA,
        handler=lambda args, **kw: research_tool_handler(args, **kw)
    )
    registry.register(
        name="predict_move",
        toolset="crowd_wisdom",
        schema=PREDICTION_TOOL_SCHEMA,
        handler=lambda args, **kw: prediction_tool_handler(args, **kw)
    )
    registry.register(
        name="risk_management",
        toolset="crowd_wisdom",
        schema=RISK_TOOL_SCHEMA,
        handler=lambda args, **kw: risk_tool_handler(args, **kw)
    )

class TradingAgent:
    def __init__(self, model: str = None):
        register_custom_tools()
        self.model = model or os.getenv("MODEL_NAME", "tencent/hy3-preview:free")
        self.agent = AIAgent(
            model=self.model,
            provider="openrouter",
            enabled_toolsets=["crowd_wisdom"],
            quiet_mode=True
        )

    def run(self, task: str):
        print(f"Agent starting task: {task}")
        response = self.agent.run_conversation(task)
        return response

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    agent = TradingAgent()
    res = agent.run("Search for BTC predictions on Polymarket and Kalshi, fetch historical data, predict the move, and calculate risk.")
    print(json.dumps(res, indent=2))
