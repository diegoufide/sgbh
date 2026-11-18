# Carga inicial de Jira

`Jira_import_HU.csv` contiene las 11 épicas (módulos) y las 89 historias de usuario del AN02 v4,
con roles y escenarios de aceptación en la descripción.

1. Crear el proyecto **SG Business Hub** con clave **SGBH** y plantilla **Scrum**.
2. Ir a **Configuración → Sistema → Importación de sistema externo → CSV** y elegir el archivo (codificación UTF-8).
3. Mapear: `Issue ID` → Issue ID, `Issue Type` → Tipo de incidencia, `Summary` → Resumen, `Epic Name` → Nombre de épica,
   `Parent` → Principal (relación con la épica), `Description` → Descripción, `Labels` → Etiquetas.
4. Revisar que queden 100 incidencias: 11 épicas y 89 historias.
