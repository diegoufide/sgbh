from uml import Diagram
d = Diagram()
pry = d.ref('Proyecto', 330, 20, stereo='ver diagrama de proyectos', w=210)
fot = d.cls('FotografiaEspacio', 20, 150, ['-rutaArchivo : String', '-descripcion : String', '-fechaHora : LocalDateTime'],
    ['+esFormatoPermitido() : boolean'])
car = d.cls('CaracteristicasTrabajo', 330, 150, ['-tipoElemento : TipoElementoVisual', '-ancho : BigDecimal', '-alto : BigDecimal',
    '-colores : String', '-material : String', '-iluminacion : Iluminacion', '-textoOLogo : String'],
    ['+calcularArea() : BigDecimal', '+estaCompleta() : boolean'])
pro = d.cls('PropuestaVisual', 690, 150, ['-nombrePropuesta : String', '-rutaImagen : String', '-estadoPropuesta : EstadoPropuesta'],
    ['+marcarAprobada() : void', '+descartar() : void'])
vis = d.cls('VisualizacionIA', 20, 470, ['-prompt : String', '-imagenResultado : String', '-modeloImagen : String', '-alternativa : int',
    '-favorita : boolean', '-fechaHora : LocalDateTime', '-usuario : String', '-tiempoRespuestaMs : int'],
    ['+marcarFavorita() : void'], stereo='registro de uso de IA')
cfg = d.cls('ConfigIA', 450, 470, ['-proveedorIa : String', '-modeloImagen : String', '-apiKeyCifrada : String', '-plantillaPrompt : String',
    '-limiteMensualImagenes : int', '-imagenesReferencia : List<String>'],
    ['+construirPrompt(c : CaracteristicasTrabajo) : String', '+limiteAlcanzado(usadas : int) : boolean', '+apiKeyEnmascarada() : String'])
bus = 110
d.rel(fot, 'T', pry, 'B', 'assoc', ma='0..*', mb='1', label='del espacio de', ta=0.5, tb=(365 - 330) / 210, via=[(20 + fot.w * 0.5, bus), (365, bus)], label_pos=(200, bus - 7))
d.rel(car, 'T', pry, 'B', 'assoc', ma='0..1', mb='1', label='describe', ta=0.3, straight=True, label_side='right')
d.rel(pro, 'T', pry, 'B', 'assoc', ma='0..*', mb='1', label='propuesta de', ta=0.5, tb=(505 - 330) / 210, via=[(690 + pro.w * 0.5, bus), (505, bus)], label_pos=(705, bus - 7))
d.rel(vis, 'T', fot, 'B', 'assoc', ma='0..*', mb='1', label='generada sobre', ta=0.3, straight=True)
d.rel(vis, 'R', car, 'B', 'dep', ta=0.12, tb=0.25, label='«use» datos del prompt', label_t=0.42)
d.rel(vis, 'R', cfg, 'L', 'dep', ta=0.5, straight=True, label='«use»')
d.rel(pro, 'B', vis, 'B', 'assoc', ma='0..1', mb='0..1', label='basada en', ta=0.85, tb=0.5, via=[(690 + pro.w * 0.85, 718), (110, 718)], label_pos=(560, 711))
y = 760
xs = 20
for name, lits in [('TipoElementoVisual', ['ROTULO_LUMINOSO', 'LETRAS_3D', 'FACHADA', 'VINILO', 'SENALIZACION']),
                   ('Iluminacion', ['NINGUNA', 'INTERNA', 'EXTERNA']),
                   ('EstadoPropuesta', ['PRESENTADA', 'APROBADA_POR_CLIENTE', 'DESCARTADA'])]:
    b = d.enum(name, xs, y, lits)
    xs += b.w + 22
d.note(xs, y, 990 - xs, ['La imagen se genera con un modelo preentrenado', 'por API (IA-005): no hay entrenamiento propio.', 'La API_KEY se guarda cifrada (AES-256) y nunca', 'se muestra completa ni va a la bitácora (RNF-014).', 'Toda imagen lleva la marca "Referencia — no es el', 'diseño final" (IA-011).'])
print(d.render('img/c7.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
