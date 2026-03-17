"""Multi-agente IA para App_Recetas_Siguaraya con Novita.

Cada agente tiene una tarea clara y usa el endpoint OpenAI-compatible de Novita.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List



NOVITA_BASE_URL = os.getenv("NOVITA_BASE_URL", "https://api.novita.ai/v3/openai")
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY", "")
DEFAULT_TIMEOUT_S = float(os.getenv("NOVITA_TIMEOUT_S", "25"))


@dataclass
class AgentSpec:
    name: str
    role: str
    task: str
    model: str


AGENT_SPECS: List[AgentSpec] = [
    AgentSpec(
        name="chef_creativo",
        role="Chef creativo",
        task="Diseñar 2 recetas alineadas al objetivo del usuario, ingredientes y restricciones.",
        model=os.getenv("NOVITA_MODEL_CHEF", "meta-llama/llama-3.1-8b-instruct"),
    ),
    AgentSpec(
        name="nutri_analista",
        role="Nutricionista",
        task="Evaluar macros/calorías estimadas y proponer mejoras saludables sin romper el sabor.",
        model=os.getenv("NOVITA_MODEL_NUTRI", "meta-llama/llama-3.1-8b-instruct"),
    ),
    AgentSpec(
        name="cost_optimizer",
        role="Optimizador de costos",
        task="Reducir costo estimado por porción y sugerir sustituciones económicas y locales.",
        model=os.getenv("NOVITA_MODEL_COST", "meta-llama/llama-3.1-8b-instruct"),
    ),
    AgentSpec(
        name="meal_planner",
        role="Planificador",
        task="Generar plan semanal de preparación (batch cooking) y orden de cocina eficiente.",
        model=os.getenv("NOVITA_MODEL_PLAN", "meta-llama/llama-3.1-8b-instruct"),
    ),
    AgentSpec(
        name="safety_guard",
        role="Control de inocuidad",
        task="Revisar seguridad alimentaria, alérgenos y puntos críticos de cocción/almacenamiento.",
        model=os.getenv("NOVITA_MODEL_SAFE", "meta-llama/llama-3.1-8b-instruct"),
    ),
]


class NovitaClient:
    def __init__(self, api_key: str = NOVITA_API_KEY, base_url: str = NOVITA_BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _mock_response(self, spec: AgentSpec, user_input: Dict[str, Any]) -> str:
        """Respuesta de respaldo cuando no hay API key."""

        return (
            f"[MODO DEMO] {spec.role}: {spec.task}\n"
            f"Resumen aplicado a '{user_input.get('objetivo', 'objetivo general')}'. "
            "Configura NOVITA_API_KEY para respuestas reales del modelo."
        )

    def chat(self, spec: AgentSpec, user_input: Dict[str, Any]) -> str:
        if not self.api_key:
            return self._mock_response(spec, user_input)

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        system_prompt = (
            f"Eres {spec.role} en App_Recetas_Siguaraya. "
            f"Tu tarea es: {spec.task} "
            "Responde en español claro, accionable y en formato breve con viñetas."
        )
        user_prompt = (
            "Datos del usuario (JSON):\n"
            f"{json.dumps(user_input, ensure_ascii=False, indent=2)}"
        )

        payload = {
            "model": spec.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        }

        request_body = json.dumps(payload).encode("utf-8")
        req = __import__("urllib.request", fromlist=["request"]).Request(
            url,
            data=request_body,
            headers=headers,
            method="POST",
        )
        with __import__("urllib.request", fromlist=["urlopen"]).urlopen(req, timeout=DEFAULT_TIMEOUT_S) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        return data["choices"][0]["message"]["content"]


class Orchestrator:
    def __init__(self, client: NovitaClient | None = None) -> None:
        self.client = client or NovitaClient()

    def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        outputs: List[Dict[str, Any]] = []

        for spec in AGENT_SPECS:
            answer = self.client.chat(spec, user_input)
            outputs.append(
                {
                    "agent": spec.name,
                    "role": spec.role,
                    "task": spec.task,
                    "model": spec.model,
                    "output": answer,
                }
            )

        merged = self._merge_decision(user_input, outputs)
        return {
            "app": "App_Recetas_Siguaraya",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "inputs": user_input,
            "agent_outputs": outputs,
            "final_plan": merged,
        }

    @staticmethod
    def _merge_decision(user_input: Dict[str, Any], outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Regla simple de fusión para que n8n tenga una salida estructurada."""

        return {
            "objetivo": user_input.get("objetivo", "Plan de recetas personalizadas"),
            "acciones_recomendadas": [
                "Validar preferencias y restricciones del usuario en UI",
                "Mostrar propuesta del chef + ajustes de nutrición y costo",
                "Presentar cronograma semanal y checklist de inocuidad",
            ],
            "resumen_agentes": [
                {"agent": item["agent"], "role": item["role"], "model": item["model"]}
                for item in outputs
            ],
        }


def run_recipe_workflow(user_input: Dict[str, Any]) -> Dict[str, Any]:
    return Orchestrator().run(user_input)
