"""Core multi-agent trading workflow primitives.

This module defines a lightweight, provider-agnostic set of agents that can be
called from an API layer or orchestration tool (for example n8n).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class AgentResult:
    """Generic response emitted by each agent."""

    agent: str
    signal: str
    confidence: float
    reason: str
    timestamp: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "agent": self.agent,
            "signal": self.signal,
            "confidence": round(self.confidence, 3),
            "reason": self.reason,
            "timestamp": self.timestamp,
        }


class BaseAgent:
    name = "base_agent"

    def evaluate(self, market_data: Dict[str, float]) -> AgentResult:
        raise NotImplementedError

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()


class TrendAgent(BaseAgent):
    name = "trend_agent"

    def evaluate(self, market_data: Dict[str, float]) -> AgentResult:
        fast = market_data.get("ema_fast", 0.0)
        slow = market_data.get("ema_slow", 0.0)
        delta = fast - slow

        if delta > 0:
            signal = "BUY"
            confidence = min(0.99, 0.6 + abs(delta) / max(1.0, abs(slow)))
            reason = "EMA rápida está por encima de la EMA lenta."
        elif delta < 0:
            signal = "SELL"
            confidence = min(0.99, 0.6 + abs(delta) / max(1.0, abs(slow)))
            reason = "EMA rápida está por debajo de la EMA lenta."
        else:
            signal = "HOLD"
            confidence = 0.5
            reason = "No hay diferencia entre EMA rápida y lenta."

        return AgentResult(self.name, signal, confidence, reason, self._now())


class RiskAgent(BaseAgent):
    name = "risk_agent"

    def evaluate(self, market_data: Dict[str, float]) -> AgentResult:
        volatility = market_data.get("volatility", 0.0)

        if volatility > 0.05:
            signal = "HOLD"
            confidence = 0.85
            reason = "Volatilidad elevada, conviene evitar entrada."
        elif volatility < 0.015:
            signal = "BUY"
            confidence = 0.7
            reason = "Volatilidad baja, entorno favorable para posición moderada."
        else:
            signal = "HOLD"
            confidence = 0.65
            reason = "Volatilidad intermedia, esperar confirmación adicional."

        return AgentResult(self.name, signal, confidence, reason, self._now())


class SentimentAgent(BaseAgent):
    name = "sentiment_agent"

    def evaluate(self, market_data: Dict[str, float]) -> AgentResult:
        score = market_data.get("sentiment_score", 0.0)

        if score >= 0.25:
            signal = "BUY"
            confidence = min(0.95, 0.55 + score)
            reason = "Sentimiento de mercado claramente positivo."
        elif score <= -0.25:
            signal = "SELL"
            confidence = min(0.95, 0.55 + abs(score))
            reason = "Sentimiento de mercado claramente negativo."
        else:
            signal = "HOLD"
            confidence = 0.55
            reason = "Sentimiento neutral o ambiguo."

        return AgentResult(self.name, signal, confidence, reason, self._now())


class DecisionAgent:
    """Combines agent outputs into a final action."""

    def aggregate(self, results: List[AgentResult]) -> Dict[str, object]:
        score_map = {"BUY": 1, "HOLD": 0, "SELL": -1}

        weighted = 0.0
        weight_sum = 0.0
        for result in results:
            weighted += score_map.get(result.signal, 0) * result.confidence
            weight_sum += result.confidence

        normalized = (weighted / weight_sum) if weight_sum else 0.0

        if normalized > 0.2:
            decision = "BUY"
        elif normalized < -0.2:
            decision = "SELL"
        else:
            decision = "HOLD"

        return {
            "decision": decision,
            "score": round(normalized, 4),
            "agents": [r.to_dict() for r in results],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def run_multi_agent_workflow(market_data: Dict[str, float]) -> Dict[str, object]:
    """Entrypoint used by the API and by external orchestrators (n8n)."""

    agents: List[BaseAgent] = [TrendAgent(), RiskAgent(), SentimentAgent()]
    results = [agent.evaluate(market_data) for agent in agents]
    return DecisionAgent().aggregate(results)
