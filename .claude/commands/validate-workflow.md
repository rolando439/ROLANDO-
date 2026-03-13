Valida la estructura del workflow n8n actual.

1. Lee el archivo `workflows/create-multi-agent-trading-workflow-in-n8n.json`.
2. Verifica:

**Estructura base**
- [ ] Campos requeridos presentes: `id`, `name`, `nodes`, `connections`, `settings`
- [ ] Todos los nodos tienen `id`, `name`, `type`, `position`, `parameters`
- [ ] No hay nodos huérfanos (sin conexiones)

**Seguridad**
- [ ] Ningún nodo tiene credenciales o API keys hardcodeadas en `parameters`
- [ ] URLs de APIs usan variables de entorno (`$env.VARIABLE`)
- [ ] No hay datos sensibles en campos de log o notificaciones

**Arquitectura de trading**
- [ ] Existe un path desde Strategy → Risk → Execution (en ese orden)
- [ ] Risk Agent tiene check explícito de `approved === true` antes de Execution
- [ ] Execution Agent NO es alcanzable si Risk rechaza la operación
- [ ] Todos los paths (éxito y rechazo) llegan al Notifier

**Error handling**
- [ ] Existe manejo de error para nodos HTTP Request (market data y broker)
- [ ] Los errores no silenciados — siempre notificados

3. Reporta resultado con checkboxes actualizados y descripción de cada problema encontrado.
