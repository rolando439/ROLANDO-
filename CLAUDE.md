# ASESOR DE TRADING — Multi-Agent AI (n8n)

## Proyecto
Workflow de trading multi-agente construido en **n8n**. Cadena de decisión:
```
Trigger → Config → [Market Data + News Data]
  → Agente Análisis Técnico (DeepSeek V3 + indicadores)   ┐
  → Agente Análisis Fundamental (Claude Opus 4.6)          ├─→ Merge
  → Agente Sentimiento Mercado (DeepSeek V3 + NewsAPI)    ┘
  → Agente Evaluación Riesgo (DeepSeek R1)
  → Agente Estrategia (Claude Sonnet 4.6)
  → Agente Decisión Final (Claude Opus 4.6)
  → Switch (BUY / SELL / HOLD)
  → Ejecutar BUY | Ejecutar SELL | HOLD
  → Notificador Telegram
```

## Stack
- n8n (JSON workflows, Code nodes v2 con `fetch()`)
- JavaScript en nodos Code
- Binance API (market data), NewsAPI (sentimiento)
- DeepSeek API (técnico, sentimiento, riesgo)
- Anthropic API (fundamental, estrategia, decisión)

## Variables de entorno requeridas
| Variable | Descripción |
|----------|-------------|
| `DEEPSEEK_API_KEY` | DeepSeek |
| `ANTHROPIC_API_KEY` | Claude Opus/Sonnet |
| `SYMBOL` | Par de trading (ej: BTCUSDT) |
| `TIMEFRAME` | Intervalo (ej: 1h) |
| `NEWS_API_KEY` | NewsAPI.org |
| `BROKER_ORDER_URL` | Endpoint del broker |
| `BROKER_API_KEY` | Clave del broker |
| `TELEGRAM_BOT_TOKEN` | Bot de Telegram |
| `TELEGRAM_CHAT_ID` | Chat destino |
| `RISK_MAX_POSITION_USD` | Ej: 1000 |
| `RISK_MAX_DRAWDOWN_PCT` | Ej: 2.5 |
| `CONFIDENCE_THRESHOLD` | Ej: 0.55 |
| `DRY_RUN` | `true` para simulación |

## Reglas
- Idioma: **español**. Código y JSON: **inglés**.
- `DRY_RUN=true` siempre al desarrollar/testear. Nunca desactivar sin backtest validado.
- Leer archivos antes de editar. No modificar `.json` sin validar estructura n8n.
- Nunca hardcodear credenciales — siempre `$env.VARIABLE`.
- Cualquier cambio en Risk o Execution requiere validación explícita.
- Commits solo cuando el usuario los solicite.

## Archivo principal
`workflows/asesor-trading-multi-agent.json`

## Comandos disponibles
| Comando | Descripción |
|---------|-------------|
| `/add-agent` | Scaffold de nuevo agente al flujo |
| `/validate-workflow` | Valida estructura del JSON n8n |
| `/risk-review` | Revisa parámetros de riesgo |
| `/backtest-plan` | Genera plan de backtesting |
| `/review` | Revisión general de cambios |
