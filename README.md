# antigravity-proyecto (integración multi‑agente)

Reescritura base para integrar un flujo **"Create multi-agent trading workflow in n8n"** con una API en Python.

## Archivos clave

- `agent.py`: lógica de agentes (tendencia, riesgo, sentimiento) + agregador de decisión.
- `api.py`: API FastAPI con endpoint `/trade/decision`.
- `app.py`: entrypoint para correr el servicio con Uvicorn.
- `n8n/workflows/multi_agent_trading_workflow.json`: workflow importable en n8n.

## Cómo correr

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Prueba rápida

```bash
curl -X POST http://localhost:8000/trade/decision \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "ema_fast": 67100,
    "ema_slow": 66600,
    "volatility": 0.018,
    "sentiment_score": 0.30
  }'
```

## Integración con n8n

1. Importa `n8n/workflows/multi_agent_trading_workflow.json`.
2. Verifica en el nodo **Call Multi-Agent API** que el método HTTP esté en `POST` (este repo ya lo define explícitamente para evitar conflictos al importar).
3. Publica la API Python para que n8n pueda accederla.
4. Envía un `POST` al webhook de n8n `/webhook/trading-signal` con el body de mercado.
5. n8n reenvía el payload al endpoint `/trade/decision` y devuelve la respuesta final.
