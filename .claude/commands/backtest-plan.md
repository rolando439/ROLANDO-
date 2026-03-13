Genera un plan de backtesting para la estrategia de trading actual.

1. Lee el workflow JSON y extrae:
   - Lógica de señal del Strategy Agent (SMA crossover + parámetros).
   - Parámetros de riesgo del Risk Agent.
   - Símbolo y timeframe configurados.

2. Define el plan de backtesting:

**Datos históricos necesarios**
- Símbolo, timeframe y rango de fechas recomendado (mínimo 1 año).
- Fuente de datos sugerida (Binance API, Yahoo Finance, etc.).
- Campos requeridos: timestamp, open, high, low, close, volume.

**Métricas a calcular**
- [ ] Total de señales generadas (BUY/SELL/HOLD)
- [ ] Señales aprobadas por Risk vs. rechazadas
- [ ] Win rate (% de operaciones rentables)
- [ ] Profit factor (ganancia total / pérdida total)
- [ ] Max drawdown
- [ ] Sharpe ratio (si hay datos suficientes)

**Casos de prueba específicos**
- Mercado en tendencia alcista fuerte.
- Mercado en tendencia bajista fuerte.
- Mercado lateral (alto número de falsos positivos esperado con SMA crossover).
- Alta volatilidad (crashes/pumps).

**Implementación sugerida**
- Script Python con `pandas` + `backtrader` o `vectorbt`.
- O sub-workflow n8n con datos históricos mock.

3. Entregar el plan como checklist accionable con código skeleton si aplica.

Nota: NO habilitar en producción sin completar el backtest y validar que las métricas son aceptables.
