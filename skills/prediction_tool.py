import sys
import os
import json
import pandas as pd
import torch
from typing import Dict, Any, List

# Add the project root to sys.path to import kronos_model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model_utils.kronos_model import Kronos, KronosTokenizer, KronosPredictor

_tokenizers = {}
_models = {}

def get_kronos_components(model_id: str = "NeoQuasar/Kronos-small"):
    if model_id not in _models:
        try:
            tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
            model = Kronos.from_pretrained(model_id)
            _tokenizers[model_id] = tokenizer
            _models[model_id] = model
        except Exception as e:
            return None, None, str(e)
    return _models[model_id], _tokenizers[model_id], None

def predict_move(df: pd.DataFrame, pred_len: int = 5) -> Dict[str, Any]:
    """
    Predicts the next up/down move using Kronos.
    """
    model, tokenizer, error = get_kronos_components()
    if error:
        # Return mock if model fails to load
        last_close = df['close'].iloc[-1]
        return {
            "prediction": "up" if last_close % 2 == 0 else "down",
            "confidence": 0.55,
            "error": f"Kronos loading failed: {error}. Using heuristic fallback."
        }

    predictor = KronosPredictor(model, tokenizer)
    
    # Convert timestamp to datetime if present
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
    else:
        df.index = pd.to_datetime(df.index)
        
    x_timestamp = df.index
    # Generate future timestamps
    last_ts = df.index[-1]
    y_timestamp = pd.date_range(start=last_ts + pd.Timedelta(minutes=5), periods=pred_len, freq='5min')
    
    try:
        pred_df = predictor.predict(df, x_timestamp, y_timestamp, pred_len=pred_len, verbose=False)
        
        last_price = df['close'].iloc[-1]
        pred_price = pred_df['close'].iloc[-1]
        
        direction = "up" if pred_price > last_price else "down"
        confidence = 0.6 # Placeholder for confidence from model variance if we had it
        
        return {
            "prediction": direction,
            "current_price": float(last_price),
            "predicted_price": float(pred_price),
            "confidence": confidence,
            "pred_len": pred_len
        }
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

def prediction_tool_handler(args: Dict[str, Any], **kwargs) -> str:
    asset = args.get("asset", "BTC")
    ohlcv_data = args.get("ohlcv_data", [])
    
    # Smart Fallback: If no data passed, fetch it now
    if not ohlcv_data:
        from skills.research_tool import fetch_crypto_history
        symbol = f"{asset}USDT"
        ohlcv_data = fetch_crypto_history(symbol, interval="5m", limit=1000)
    
    if not ohlcv_data or (isinstance(ohlcv_data, list) and len(ohlcv_data) > 0 and "error" in ohlcv_data[0]):
        return json.dumps({"error": "Failed to retrieve OHLCV data for prediction."})
    
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(ohlcv_data)
    res = predict_move(df)
    res["asset"] = asset
    
    return json.dumps(res, indent=2)

PREDICTION_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "predict_move",
        "description": "Predict the next price movement (up/down) for a crypto asset using Kronos model.",
        "parameters": {
            "type": "object",
            "properties": {
                "asset": {
                    "type": "string",
                    "description": "The crypto asset (BTC, ETH)."
                },
                "ohlcv_data": {
                    "type": "array",
                    "description": "Historical OHLCV data points.",
                    "items": { "type": "object" }
                }
            },
            "required": ["asset"]
        }
    }
}
