Revisa todos los archivos modificados en el working tree actual.

1. Ejecuta `git diff` y `git status` para ver los cambios.
2. Para cada archivo modificado, léelo completo.
3. Si hay archivos `.json` en `workflows/`, aplica validación de estructura n8n.
4. Si hay código JavaScript (nodos Function/Code), aplica revisión de expresiones n8n y lógica de trading.

Reporta:
- **Archivos revisados**
- **Problemas críticos** (bugs, seguridad, lógica de riesgo rota)
- **Advertencias** (anti-patrones, falta de error handling)
- **Veredicto**: listo para commit / necesita cambios

Sé directo. Prioriza los problemas que afectan la seguridad del capital.
