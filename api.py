"""API para acoplar multi-agente IA en App_Recetas_Siguaraya."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import AGENT_SPECS, run_recipe_workflow


class RecipeWorkflowPayload(BaseModel):
    usuario_id: str = Field(..., description="ID del usuario en App_Recetas_Siguaraya")
    objetivo: str = Field(default="Comer saludable y ahorrar tiempo")
    ingredientes_disponibles: List[str] = Field(default_factory=list)
    restricciones: List[str] = Field(default_factory=list)
    alergias: List[str] = Field(default_factory=list)
    presupuesto_semanal: Optional[float] = None
    porciones_por_receta: int = 2
    metadata: Optional[Dict[str, Any]] = None


app = FastAPI(title="App_Recetas_Siguaraya Multi-Agent API", version="2.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "recetas-multiagente"}


@app.get("/agents")
def list_agents() -> Dict[str, object]:
    return {
        "count": len(AGENT_SPECS),
        "agents": [
            {"name": a.name, "role": a.role, "task": a.task, "model": a.model}
            for a in AGENT_SPECS
        ],
    }


@app.post("/recipes/workflow")
def recipes_workflow(payload: RecipeWorkflowPayload) -> Dict[str, Any]:
    data = payload.model_dump()
    result = run_recipe_workflow(data)
    return {
        "usuario_id": payload.usuario_id,
        "result": result,
        "metadata": payload.metadata or {},
    }
