Revisa la configuración de riesgo del workflow de trading.

1. Lee el workflow JSON y extrae la lógica del Risk Agent.
2. Evalúa los parámetros actuales:
   - `RISK_MAX_POSITION_USD`: ¿es conservador para el símbolo operado?
   - `RISK_MAX_DRAWDOWN_PCT`: ¿está alineado con la tolerancia al riesgo?
   - `CONFIDENCE_THRESHOLD` (0.55): ¿es suficientemente alto para filtrar señales débiles?

3. Verifica la lógica de filtrado:
   - ¿Cubre los tres casos de bloqueo: tamaño, drawdown, confianza?
   - ¿Hay casos límite donde `approved` podría ser `undefined` en lugar de `false`?
   - ¿El agente de Risk puede recibir datos malformados desde Strategy sin romperse?

4. Señala mejoras de riesgo comunes:
   - ¿Falta un circuit breaker (parar después de N pérdidas consecutivas)?
   - ¿Falta un check de horario (no operar fuera de mercado)?
   - ¿Falta validación de liquidez mínima?

5. Entrega:
   - **Estado actual**: parámetros y lógica vigente
   - **Vulnerabilidades de riesgo**: situaciones donde el filtro podría fallar
   - **Recomendaciones** con impacto estimado (conservador / moderado / agresivo)

Advertencia importante: cualquier cambio en Risk Agent debe ser validado con backtesting antes de producción.
