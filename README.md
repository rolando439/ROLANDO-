# App_Recetas_Siguaraya + Multiagente IA (Novita)

Esta versión acopla el sistema multiagente directamente a **App_Recetas_Siguaraya**.

## Agentes IA y tareas (Novita API Key)

1. **chef_creativo**: crea recetas base según objetivo, restricciones e ingredientes.
2. **nutri_analista**: mejora perfil nutricional.
3. **cost_optimizer**: reduce costo por porción con sustituciones.
4. **meal_planner**: organiza plan semanal y batch cooking.
5. **safety_guard**: valida inocuidad, alérgenos y puntos críticos.

Todos se configuran con `NOVITA_API_KEY` y puedes asignar modelo por agente:

- `NOVITA_MODEL_CHEF`
- `NOVITA_MODEL_NUTRI`
- `NOVITA_MODEL_COST`
- `NOVITA_MODEL_PLAN`
- `NOVITA_MODEL_SAFE`

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export NOVITA_API_KEY="tu_api_key"
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /health`
- `GET /agents` (lista agentes + tareas + modelo)
- `POST /recipes/workflow`

## Ejemplo payload

```json
{
  "usuario_id": "u-1001",
  "objetivo": "Bajar grasa y cocinar en menos de 40 minutos",
  "ingredientes_disponibles": ["pollo", "arroz", "tomate", "espinaca"],
  "restricciones": ["sin frituras"],
  "alergias": ["maní"],
  "presupuesto_semanal": 35,
  "porciones_por_receta": 3
}
```

## n8n

Importa `n8n/workflows/multi_agent_trading_workflow.json` (nombre histórico del archivo) y usa el webhook:

- `POST /webhook/recetas-siguaraya`

Ese webhook reenvía el body a `/recipes/workflow` y devuelve la respuesta final para la app.
