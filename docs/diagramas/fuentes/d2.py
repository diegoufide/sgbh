from blocks import *
s = SVG(1000, 640)
C = [105, 300, 495, 690, 885]; W = 176
def card(c, y, code, name, hu, lines, head=BLUE, h=104):
    x = C[c] - W / 2
    s.box(x, y, W, h, name, lines, stereo=f'{code} · {hu} HU', head=head, size=11.5)
    return x, y, h
y1 = 34
card(0, y1, 'M10 · CLI', 'Clientes', 7, ['Personas y empresas,', 'contactos y expediente'])
card(1, y1, 'M3 · SOL', 'Solicitudes', 7, ['Pedido, canal, estados', 'y conversión a proyecto'])
card(2, y1, 'M2 · COT', 'Cotizaciones', 7, ['Catálogo, IVA 13 %,', 'versiones y vencimiento'])
card(3, y1, 'M1 · PRO', 'Proyectos', 10, ['Etapas, tareas, avance,', 'cierre y reapertura'])
card(4, y1, 'M5 · PRD', 'Producción y entregas', 8, ['Orden OP, etapas,', 'entrega con evidencia'])
for a, b in [(0, 1), (1, 2), (2, 3), (3, 4)]:
    xa = C[a] + W / 2; xb = C[b] - W / 2
    s.arrow([(xa, y1 + 62), (xb - 2, y1 + 62)])
y2 = 194
card(0, y2, 'M6 · COM', 'Comunicaciones', 6, ['Mensajes por canal y', 'solicitudes de cambio'], head=BLUE2)
card(3, y2, 'M4 · VIS', 'Visualización', 6, ['Fotos del espacio,', 'características, propuestas'], head=BLUE2)
card(4, y2, 'M7 · INV', 'Inventario', 9, ['Materiales, entradas, salidas,', 'proveedores y alertas'], head=BLUE2)
s.arrow([(C[0], y2), (C[0], y1 + 106)], 'cliente y proyecto', lpos=(C[0] + 6, y2 - 22), lanchor='start', dashed=True, size=10.5)
s.arrow([(C[3], y2), (C[3], y1 + 106)], 'del proyecto', lpos=(C[3] + 6, y2 - 22), lanchor='start', dashed=True, size=10.5)
s.arrow([(C[4], y2), (C[4], y1 + 106)], 'materiales', lpos=(C[4] + 6, y2 - 22), lanchor='start', dashed=True, size=10.5)
y3 = 384
s.box(20, y3, 755, 136, 'Inteligencia Artificial', [], stereo='M11 · IA · 15 HU', head='#1E2466')
cols = [('Entrenamiento (IA-001 a IA-007)', ['Conjunto de datos sin datos', 'personales, 3 modelos, versiones', 'y reentrenamiento automático']),
        ('Uso (IA-008 a IA-013)', ['Riesgo de atraso y alertas, sugerir', 'cotización, visualizar con IA', 'generativa, clasificar mensajes']),
        ('Control (IA-014 y IA-015)', ['Panel de desempeño y uso,', 'bitácora de modelos, datos', 'y configuración'])]
for i, (t, ls) in enumerate(cols):
    x = 32 + i * 248
    s.text(x, y3 + 62, t, 12, 'bold', 'start', color=BLUE)
    for j, ln in enumerate(ls):
        s.text(x, y3 + 80 + j * 16, ln, 11.5, anchor='start')
s.arrow([(C[0], y3), (C[0], y2 + 106)], 'clasifica', lpos=(C[0] + 6, y3 - 14), lanchor='start', dashed=True, size=10.5)
s.arrow([(C[2], y3), (C[2], y1 + 106)], 'sugiere ítems', lpos=(C[2] - 6, y3 - 14), lanchor='end', dashed=True, size=10.5)
s.arrow([(590, y3), (590, y1 + 120), (C[3] - 40, y1 + 120), (C[3] - 40, y1 + 106)], 'riesgo de atraso', lpos=(596, y3 - 30), lanchor='start', dashed=True, size=10.5)
s.arrow([(C[3], y3), (C[3], y2 + 106)], 'genera imagen', lpos=(C[3] + 6, y3 - 14), lanchor='start', dashed=True, size=10.5)
card(4, y3, 'M9 · REP', 'Reportes y tablero', 6, ['Indicadores, gráficos,', 'PDF/Excel. Lee todos los', 'módulos (solo lectura)'], head=BLUE2, h=136)
y4 = 548
s.rect(20, y4, 950, 76, fill='#FFF8E6', stroke=ORANGE, rx=8)
s.text(34, y4 + 22, 'Transversal · M8 · SEG · 8 HU — Usuarios y seguridad', 13.5, 'bold', 'start', color='#7C2D12')
s.text(34, y4 + 42, 'Inicio de sesión (bloqueo tras 5 intentos), recuperación de contraseña, roles y permisos, control de acceso por URL,', 11.5, anchor='start')
s.text(34, y4 + 58, 'sesión de 30 min. Servicios compartidos por todos los módulos: bitácora de solo inserción y notificaciones internas.', 11.5, anchor='start')
s.render('img/d2.png')
