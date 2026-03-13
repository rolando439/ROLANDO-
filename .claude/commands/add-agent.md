Scaffold de un nuevo agente para el workflow de trading en n8n.

1. Pregunta al usuario:
   - Nombre del agente y su responsabilidad en el flujo.
   - Qué datos recibe (input) y qué datos entrega (output).
   - Dónde se conecta en la cadena actual: Orchestrator → Strategy → Risk → Execution → Notifier.

2. Genera el bloque JSON del agente con:
   - Nodo trigger/input (normalmente un nodo `Set` o recibe de nodo anterior).
   - Nodo `Code` con la lógica del agente (placeholder con comentarios explicativos).
   - Nodo de output con el contrato de datos documentado.
   - Nodo de error handling conectado al Notifier.

3. Indica exactamente cómo integrarlo al JSON principal del workflow:
   - Nodos a agregar en el array `nodes`.
   - Conexiones a agregar/modificar en `connections`.

4. Proporciona un ejemplo de datos de prueba (mock input) para testear el agente de forma aislada.

Principios:
- Un agente = una responsabilidad.
- Nunca saltarse el Risk Agent para llegar a Execution.
- Siempre conectar el path de error al Notifier.
