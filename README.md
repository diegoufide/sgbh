# SG Business Hub

Sistema web de gestión para **SG Soluciones 506** (comunicación visual, Ciudad Colón, Costa Rica):
clientes, solicitudes, cotizaciones, proyectos, producción, inventario, comunicaciones, visualización de espacios,
reportes e inteligencia artificial.

Proyecto del curso **SC-603 Análisis y Modelado de Requerimientos** — Universidad Fidélitas — Grupo 7.

| Integrante | Rol en el proyecto |
|---|---|
| Jordan Ivan Soto Morales | Coordinación y análisis de requerimientos |
| Rodrigo Josuel Rodríguez Jiménez | Análisis tecnológico |
| Johan Solís López | Documentación y análisis operativo (contacto con el patrocinador) |
| Diego Morales López | Análisis de procesos |

## Arquitectura

Monolito modular en capas (**Java 21 + Spring Boot 4.1 + Thymeleaf + Bootstrap 5.3 + PostgreSQL 16**) con un servicio
de IA independiente (**Python 3.12 + FastAPI + scikit-learn**), desplegados con Docker Compose detrás de Nginx.
El detalle completo está en [`docs/arquitectura/G7_SC603_K_Arquitectura.pdf`](docs/arquitectura/G7_SC603_K_Arquitectura.pdf).

```
sgbh/
├── sgbh-web/      Aplicación principal Spring Boot (paquete base cr.sgsoluciones506.businesshub)
├── ia-service/    Servicio de IA (FastAPI): atrasos, sugerencias de cotización y clasificación de mensajes
├── infra/         docker-compose.yml, Nginx, variables de entorno de ejemplo y script de respaldo
├── docs/          Documento de arquitectura, diagramas, decisiones y carga inicial de Jira
└── .github/       Integración continua y plantilla de pull request
```

## Ejecutar en desarrollo

Requisitos: JDK 21, Maven 3.9, Python 3.12 y Docker.

```bash
cp infra/.env.example infra/.env          # completar las claves
docker compose -f infra/docker-compose.yml up -d sgbh-db
mvn -f sgbh-web/pom.xml spring-boot:run -Dspring-boot.run.profiles=dev
cd ia-service && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
```

Pruebas: `mvn -f sgbh-web/pom.xml verify` y `pytest ia-service/tests`.

## Flujo de trabajo

- Ramas: `main` (producción), `develop` (integración), `feature/SGBH-<n>-<descripcion>`, `release/<x.y>`, `hotfix/SGBH-<n>-<descripcion>`.
- Commits: `SGBH-<n> <verbo en presente> <qué>` — por ejemplo `SGBH-12 Agrega validación de cédula duplicada`.
- Todo cambio entra por pull request a `develop` con 1 aprobación y la integración continua en verde.
- Las tareas viven en Jira (proyecto **SGBH**); la clave en ramas, commits y PR los vincula automáticamente.
- Versiones con SemVer: `v1.0.0`.
