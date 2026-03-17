"""FastAPI endpoints for the multi-agent trading workflow."""

from __future__ import annotations

from typing import Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import run_multi_agent_workflow


class MarketPayload(BaseModel):
    symbol: str = Field(default="BTCUSDT", description="Trading pair symbol")
    ema_fast: float = 0.0
    ema_slow: float = 0.0
    volatility: float = 0.02
    sentiment_score: float = 0.0
    metadata: Optional[Dict[str, str]] = None


app = FastAPI(title="Multi-Agent Trading API", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/trade/decision")
def trade_decision(payload: MarketPayload) -> Dict[str, object]:
    data = payload.model_dump()
    result = run_multi_agent_workflow(data)
    return {
        "symbol": payload.symbol,
        "result": result,
        "metadata": payload.metadata or {},
    }
