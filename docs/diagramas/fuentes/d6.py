from blocks import *
s = SVG(1000, 492)
s.group(10, 10, 770, 120, 'Jira Software · proyecto SGBH (plantilla Scrum)')
states = [('Por hacer', 90), ('En curso', 260), ('En revisión', 470), ('Hecho', 690)]
for i, (t, cx) in enumerate(states):
    s.rect(cx - 70, 58, 140, 46, fill=LIGHT if i < 3 else '#E7F6EC', stroke=BLUE if i < 3 else '#15803D', rx=8)
    s.text(cx, 79, t, 13.5, 'bold', color=BLUE if i < 3 else '#15803D')
    s.text(cx, 96, 'SGBH-12', 11, color=GRAY)
    if i < 3:
        s.arrow([(cx + 70, 81), (states[i + 1][1] - 72, 81)])
s.note(796, 14, 194, ['Reglas del repositorio:', '· main y develop protegidas', '· PR con 1 aprobación', '· CI en verde para fusionar', '· sin push directo a main'], size=11)
lanes = [('feature/SGBH-12-…', 230), ('develop', 300), ('release/1.0', 370), ('main', 440)]
for t, y in lanes:
    s.text(20, y + 4, t, 12, 'bold', 'start', color=BLUE if t != 'main' else '#15803D')
    s.mid.append(f'<path d="M150,{y} H975" stroke="#D1D5DB" stroke-width="1" stroke-dasharray="3 4"/>')
def line(pts, color=BLUE, w=3):
    s.mid.append(f'<path d="M' + ' L'.join(f'{x},{y}' for x, y in pts) + f'" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>')
def dot(x, y, label=None, color=BLUE, above=True, tag=False):
    s.front.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="{color}" stroke-width="3"/>')
    if label:
        s.text(x, y - 13 if above else y + 22, label, 10.5, color=INK, italic=not tag, halo=True, weight='bold' if tag else 'normal')
line([(165, 300), (975, 300)])
line([(165, 440), (975, 440)], '#15803D')
line([(200, 300), (240, 230), (480, 230), (560, 300)], '#7C3AED')
line([(640, 300), (680, 370), (760, 370), (800, 440)], '#C2410C')
line([(760, 370), (820, 300)], '#C2410C', 2)
dot(180, 440, 'v0.1.0', '#15803D', above=False, tag=True)
dot(180, 300); dot(240, 230, 'crea rama', '#7C3AED', above=False); dot(330, 230, 'SGBH-12 entidad Cliente', '#7C3AED'); dot(395, 230, 'SGBH-12 validaciones', '#7C3AED', above=False)
dot(560, 300, 'merge PR', above=False); dot(640, 300); dot(720, 370, 'ajustes QA', '#C2410C', above=False)
dot(800, 440, 'v1.0.0', '#15803D', above=False, tag=True); dot(820, 300); dot(900, 300)
s.rect(452, 214, 36, 32, fill='#fff', stroke='#7C3AED', sw=2, rx=4)
s.text(470, 235, 'PR', 12, 'bold', color='#7C3AED')
s.arrow([(240, 222), (240, 150), (260, 150), (260, 106)], 'rama creada', lpos=(266, 140), lanchor='start', dashed=True, size=10.5)
s.arrow([(470, 212), (470, 106)], 'PR abierto + CI', lpos=(476, 160), lanchor='start', dashed=True, size=10.5)
s.arrow([(560, 292), (560, 160), (690, 160), (690, 106)], 'PR fusionado', lpos=(696, 140), lanchor='start', dashed=True, size=10.5)
s.text(500, 486, 'Las ramas, commits y PR llevan la clave de la historia (SGBH-12): la app GitHub for Atlassian los muestra en la historia y las reglas de automatización mueven el estado.', 11, color=GRAY, italic=True)
s.render('img/d6.png')
