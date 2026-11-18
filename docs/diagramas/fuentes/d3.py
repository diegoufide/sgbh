from blocks import *
s = SVG(1000, 560)
bands = [('1. Presentación', 'Thymeleaf 3 (plantillas y fragmentos de layout) · Bootstrap 5.3', 'Bootstrap Icons · Chart.js 4 · JavaScript (fetch a /api)', 'templates/, static/'),
         ('2. Controladores', '@Controller para vistas · @RestController para /api/**', 'DTO y formularios con Bean Validation (@Valid) · @ControllerAdvice', '*Controller, *Form, *Dto'),
         ('3. Servicios (negocio)', '@Service + @Transactional: reglas de negocio (IVA 13 %, vigencia,', 'existencias, estados) · eventos de dominio · tareas @Scheduled', '*Service, *ServiceImpl'),
         ('4. Acceso a datos', 'Spring Data JPA (Hibernate 6) · entidades @Entity · consultas', 'derivadas y @Query · migraciones versionadas con Flyway', '*Repository, db/migration'),
         ('5. Datos', 'PostgreSQL 16 (esquema sgbh) · volumen de archivos (fotos,', 'evidencias, PDF) · modelos de IA serializados (.joblib)', 'sgbh-db, volúmenes')]
y = 20; H = 86; G = 18
for i, (t, l1, l2, pk) in enumerate(bands):
    s.rect(70, y, 640, H, fill='#fff', stroke=BLUE, rx=6)
    s.mid.append(f'<path d="M76,{y} h164 v{H} h-164 a6,6 0 0 1 -6,-6 v{-H+12} a6,6 0 0 1 6,-6 z" fill="{BLUE if i < 4 else "#1E2466"}"/>')
    s.text(155, y + 38, t, 13.5, 'bold', color='#fff')
    s.text(155, y + 58, pk, 11, color='#C7CBF0', italic=True)
    s.text(254, y + 34, l1, 12, anchor='start')
    s.text(254, y + 54, l2, 12, anchor='start')
    if i < 4:
        s.arrow([(44, y + H / 2), (44, y + H + G + H / 2 - 2)], head=True) if False else None
        s.arrow([(390, y + H), (390, y + H + G - 1)])
    y += H + G
s.arrow([(40, 60), (40, 470)])
s.mid.append('<text x="40" y="275" font-size="11.5" fill="#1F2340" font-style="italic" text-anchor="middle" transform="rotate(-90 40 275)" paint-order="stroke" stroke="#fff" stroke-width="5">cada capa solo invoca a la de abajo</text>')
s.rect(735, 20, 245, 294, fill='#FFF8E6', stroke=ORANGE, rx=8)
s.text(857, 44, 'Transversal', 14, 'bold', color='#7C2D12')
tl = [('Seguridad', 'Spring Security: BCrypt, CSRF,'), ('', 'sesión 30 min, @PreAuthorize'), ('Auditoría', '@Auditable (AOP) → bitácora'),
      ('', 'en la misma transacción'), ('Notificaciones', 'internas y por correo'), ('Errores y logs', '@ControllerAdvice · SLF4J'), ('', 'Logback (JSON en prd)'), ('Configuración', 'perfiles dev · qa · prd')]
yy = 72
for a, b in tl:
    if a: s.text(749, yy, a, 12, 'bold', 'start', color='#7C2D12'); yy += 16
    s.text(749, yy, b, 11.5, anchor='start'); yy += 17
s.rect(735, 332, 245, 194, fill=LIGHT, stroke=BLUE2, rx=8)
s.text(857, 356, 'Integración (paquete integracion)', 13, 'bold', color=BLUE)
il = [('IaServiceClient', 'RestClient → sgbh-ia (FastAPI)'), ('ImagenIaClient', 'API externa de imágenes'), ('CorreoService', 'JavaMailSender (SMTP)'), ('Documentos', 'OpenPDF · Apache POI (Excel)')]
yy = 382
for a, b in il:
    s.text(749, yy, a, 12, 'bold', 'start', color=BLUE); yy += 16
    s.text(749, yy, b, 11.5, anchor='start'); yy += 20
s.arrow([(710, 236), (733, 236)])
s.render('img/d3.png')
