from blocks import *
s = SVG(1000, 650)
s.package(10, 10, 980, 630, 'sgbh  (repositorio GitHub · monorepo)', fill='#FBFBFE', tab_w=300)
s.package(28, 50, 690, 572, 'sgbh-web  ·  cr.sgsoluciones506.businesshub', fill='#fff', tab_w=330)
s.rect(42, 86, 662, 236, fill='#F7F8FC', stroke=BLUE2, sw=1, rx=6, dash='5 4', layer='mid')
s.text(54, 104, 'Módulos de negocio', 12, 'bold', 'start', color=BLUE2)
mods = [('cliente', 'Cliente, ContactoCliente'), ('solicitud', 'Solicitud, ArchivoAdjunto'), ('cotizacion', 'Cotizacion, ElementoCatalogo'),
        ('proyecto', 'Proyecto, Tarea'), ('produccion', 'OrdenProduccion, Entrega'), ('comunicacion', 'Comunicacion, SolicitudCambio'),
        ('inventario', 'Material, Movimiento, Proveedor'), ('visualizacion', 'FotografiaEspacio, Propuesta'), ('reporte', 'Tablero, exportaciones')]
for i, (n, l) in enumerate(mods):
    x = 54 + (i % 3) * 216; y = 116 + (i // 3) * 68
    s.package(x, y, 204, 56, n, [l], tab_w=len(n) * 8 + 18)
s.package(262, 350, 196, 70, 'ia', ['Modelos, predicciones,', 'sugerencias, ConfigIA'], tab_w=40)
s.package(494, 350, 196, 70, 'integracion', ['IaServiceClient, ImagenIaClient,', 'CorreoService, PdfGenerator'], tab_w=100)
s.package(54, 350, 196, 70, 'config', ['SecurityConfig, WebConfig,', 'SchedulingConfig'], tab_w=62)
s.rect(42, 448, 662, 104, fill='#FFF8E6', stroke=ORANGE, sw=1, rx=6, dash='5 4', layer='mid')
s.text(54, 466, 'Transversales', 12, 'bold', 'start', color='#7C2D12')
for i, (n, l) in enumerate([('seguridad', 'Usuario, Rol, Permiso'), ('bitacora', 'Bitacora, @Auditable'), ('notificacion', 'Notificacion'), ('comun', 'EntidadAuditable, errores')]):
    s.package(54 + i * 162, 478, 152, 62, n, [l], tab_w=len(n) * 8 + 18)
s.text(54, 576, 'Cada módulo contiene los subpaquetes controller/ · service/ · repository/ · model/ · dto/', 11.5, anchor='start', italic=True, color=GRAY)
s.text(54, 594, 'Recursos: templates/<módulo>/ · static/ · db/migration/ (Flyway) · application-{dev,qa,prd}.yml', 11.5, anchor='start', italic=True, color=GRAY)
s.arrow([(476, 322), (476, 446)], '«use» (todos los módulos)', lpos=(482, 440), lanchor='start', dashed=True)
s.arrow([(330, 350), (330, 324)], '«use»', lpos=(336, 341), lanchor='start', dashed=True)
s.arrow([(458, 385), (492, 385)], dashed=True)
s.package(738, 50, 236, 200, 'ia-service', ['Python 3.12 · FastAPI', '', 'app/api/  (endpoints REST)', 'app/modelos/  (atrasos,', '    cotizaciones, mensajes)', 'app/entrenamiento/', 'app/datos/  (preparación)', 'tests/  (pytest)', 'requirements.txt · Dockerfile'], tab_w=90)
s.package(738, 270, 236, 108, 'infra', ['docker-compose.yml', 'nginx/sgbh.conf', '.env.example (sin secretos)', 'scripts/respaldo.sh'], tab_w=50)
s.package(738, 398, 236, 92, 'docs', ['arquitectura/ (este documento)', 'diagramas/ (PNG y fuentes)', 'adr/ (decisiones)'], tab_w=50)
s.package(738, 510, 236, 110, '.github', ['workflows/ci.yml', '(compilar, probar, imagen)', 'pull_request_template.md', 'CODEOWNERS'], tab_w=70)
s.arrow([(690, 400), (726, 400), (726, 150), (736, 150)], 'HTTP/JSON', lpos=(742, 264), lanchor='start', dashed=True)
s.render('img/d4.png')
