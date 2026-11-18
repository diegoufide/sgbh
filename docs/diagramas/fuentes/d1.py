from blocks import *
s = SVG(1000, 670)
s.box(20, 30, 200, 140, 'Usuarios (5 roles)', ['Administrador', 'Servicio al cliente', 'Diseñador', 'Fabricante', 'Servicios profesionales'])
s.box(20, 270, 200, 120, 'Navegador web', ['HTML5 · CSS3 · JavaScript', 'Bootstrap 5.3 (responsive)', 'Chart.js 4 (gráficos)', 'PC, tableta o celular'], stereo='cliente')
s.arrow([(120, 170), (120, 268)], 'usa', lpos=(112, 223), lanchor='end')
s.group(250, 20, 480, 635, 'Servidor sgbh-prd-srv-01', 'Ubuntu Server 24.04 LTS · Docker Compose · 2 vCPU · 8 GB RAM · SSD')
s.box(280, 62, 420, 58, 'sgbh-proxy · Nginx', ['Terminación TLS (Let\'s Encrypt) · único puerto público'], head=BLUE2, head_h=26)
s.box(280, 168, 420, 262, 'sgbh-web · Spring Boot 4.1 (Java 21)', [], head=BLUE, head_h=28)
layers = [('Presentación', 'Thymeleaf + Bootstrap 5.3 (vistas y formularios)'),
          ('Controladores', 'Spring MVC @Controller / @RestController'),
          ('Servicios', 'Reglas de negocio de los 11 módulos · @Scheduled'),
          ('Acceso a datos', 'Spring Data JPA (Hibernate) · Flyway')]
yy = 206
for t, d in layers:
    s.rect(292, yy, 292, 46, fill=LIGHT, stroke=BLUE2, sw=1, rx=4)
    s.text(302, yy + 19, t, 12.5, 'bold', 'start', color=BLUE)
    s.text(302, yy + 36, d, 11.5, anchor='start')
    yy += 54
s.rect(594, 206, 96, 208, fill='#FFF8E6', stroke=ORANGE, sw=1, rx=4)
for i, ln in enumerate(['Transversal', '', 'Spring', 'Security', '', 'Bitácora', '(AOP)', '', 'Notifica-', 'ciones']):
    s.text(642, 228 + i * 18, ln, 11.5, 'bold' if i == 0 else 'normal', color='#7C2D12')
s.box(280, 480, 195, 112, 'sgbh-db', ['PostgreSQL 16', 'Esquema sgbh (Flyway)', 'Rol sin UPDATE/DELETE', 'sobre la bitácora'], head=BLUE2, head_h=26)
s.box(505, 480, 195, 112, 'sgbh-ia · FastAPI', ['Python 3.12 · scikit-learn', 'pandas · joblib', 'Modelos: atrasos,', 'cotizaciones, mensajes'], head=BLUE2, head_h=26)
s.text(490, 636, 'Volúmenes: sgbh-datos-db · sgbh-archivos (fotos, PDF) · sgbh-modelos (.joblib)', 11.5, color=GRAY, italic=True, layer='back')
s.arrow([(220, 330), (236, 330), (236, 91), (278, 91)], 'HTTPS 443', lpos=(230, 250), lanchor='end')
s.arrow([(490, 120), (490, 166)], 'HTTP 8080 · red interna')
s.arrow([(378, 430), (378, 478)], 'JDBC 5432')
s.arrow([(602, 430), (602, 478)], 'REST/JSON 8000\n+ token interno')
s.box(800, 40, 190, 100, 'Proveedor IA de imágenes', ['API generativa externa', 'proveedor configurable', '(CONFIG_IA, IA-005)'], stereo='sistema externo', head='#3F4A5A')
s.box(800, 200, 190, 100, 'Servidor de correo', ['SMTP con TLS', 'alertas, recuperación', 'de contraseña, resúmenes'], stereo='sistema externo', head='#3F4A5A')
s.box(800, 360, 190, 100, 'Respaldo externo', ['copia diaria cifrada', 'de la BD y archivos', '(retención 30 días)'], stereo='almacenamiento', head='#3F4A5A')
s.box(800, 520, 190, 130, 'WhatsApp / redes', ['Fuera de alcance:', 'los mensajes se registran', 'a mano en el módulo de', 'comunicaciones (COM-001)'], stereo='sin integración', head='#9CA3AF', fill='#F9FAFB', dash='5 4')
s.arrow([(700, 190), (760, 190), (760, 90), (798, 90)], 'HTTPS saliente\nAPI key cifrada', lpos=(804, 162), lanchor='start')
s.arrow([(700, 250), (798, 250)], 'SMTP 587', lpos=(736, 243), lanchor='start')
s.arrow([(378, 592), (378, 612), (766, 612), (766, 410), (798, 410)], 'pg_dump diario', lpos=(772, 492), lanchor='start')
s.render('img/d1.png')
