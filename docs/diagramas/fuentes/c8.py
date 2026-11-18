from uml import Diagram
d = Diagram()
ds = d.cls('DatasetIA', 20, 20, ['-tipoModelo : TipoModelo', '-fechaInicio : LocalDate', '-fechaFin : LocalDate', '-cantidadRegistros : int',
    '-fechaGeneracion : LocalDateTime', '-rutaArchivo : String', '-estado : EstadoDataset', '-detalleError : String'],
    ['+esSuficiente() : boolean'])
mo = d.cls('ModeloIA', 350, 20, ['-tipoModelo : TipoModelo', '-version : int', '-fechaEntrenamiento : LocalDateTime',
    '-metricas : Map<String, BigDecimal>', '-rutaArchivo : String', '-estado : EstadoModelo', '-motivo : String'],
    ['+cumpleMinimo() : boolean', '+activar() : void', '+retirar(motivo : String) : void'])
pr = d.cls('ProgramacionReentrenamiento', 700, 20, ['-tipoModelo : TipoModelo', '-frecuencia : Frecuencia', '-diaEjecucion : int',
    '-minimoRegistrosNuevos : int = 50', '-activa : boolean', '-ultimaEjecucion : LocalDateTime'],
    ['+debeEjecutar(nuevos : int) : boolean'])
pe = d.cls('PrediccionIA', 20, 360, ['-probabilidadAtraso : BigDecimal', '-nivelRiesgo : NivelRiesgo', '-diasAtrasoEstimados : int',
    '-fechaEstimadaFin : LocalDate', '-fechaHora : LocalDateTime', '-recomendacionAceptada : Boolean', '-retroalimentacion : String'],
    ['_+clasificar(p : BigDecimal) : NivelRiesgo'])
su = d.cls('SugerenciaIA', 520, 360, ['-tipoModelo : TipoModelo', '-cantidadSugerida : BigDecimal', '-confianza : BigDecimal',
    '-categoria : CategoriaMensaje', '-accion : AccionSugerencia', '-fechaHora : LocalDateTime', '-tiempoRespuestaMs : int'],
    ['+registrarAccion(a : AccionSugerencia) : void'])
ta = d.ref('Tarea', 20, 690, stereo='ver proyectos', w=150)
co = d.ref('Cotizacion', 400, 690, stereo='ver cotizaciones', w=150)
el = d.ref('ElementoCatalogo', 590, 690, stereo='ver cotizaciones', w=180)
cm = d.ref('Comunicacion', 810, 690, stereo='ver clientes', w=170)
d.rel(mo, 'L', ds, 'R', 'assoc', ma='0..*', mb='1', label='entrenado con', ta=0.25, straight=True)
d.rel(pr, 'L', mo, 'R', 'dep', ta=0.3, straight=True, label='«create»')
d.rel(pe, 'T', mo, 'B', 'assoc', ma='0..*', mb='1', label='generada por', ta=0.75, tb=0.3, label_side='above')
d.rel(su, 'T', mo, 'B', 'assoc', ma='0..*', mb='1', label='generada por', ta=0.2, tb=0.7, label_t=0.35)
d.rel(pe, 'B', ta, 'T', 'assoc', ma='0..*', mb='1', label='sobre', ta=0.2, straight=True)
d.rel(su, 'B', co, 'T', 'assoc', ma='0..*', mb='0..1', label='para', ta=0.08, tb=0.6, label_side='left', label_t=0.7)
d.rel(su, 'B', el, 'T', 'assoc', ma='0..*', mb='0..1', label='sugiere', ta=0.45, tb=0.5, label_t=0.7)
d.rel(su, 'B', cm, 'T', 'assoc', ma='0..*', mb='0..1', label='clasifica', ta=0.85, tb=0.4, label_t=0.7)
y = 780
xs = 20
for name, lits in [('TipoModelo', ['ATRASOS', 'COTIZACIONES', 'MENSAJES']),
                   ('EstadoModelo', ['ENTRENADO', 'ACTIVO', 'RETIRADO', 'RECHAZADO', 'FALLIDO']),
                   ('EstadoDataset', ['LISTO', 'INSUFICIENTE']),
                   ('NivelRiesgo', ['ALTO', 'MEDIO', 'BAJO']),
                   ('AccionSugerencia', ['ACEPTADA', 'EDITADA', 'DESCARTADA']),
                   ('Frecuencia', ['MENSUAL', 'TRIMESTRAL'])]:
    b = d.enum(name, xs, y, lits)
    xs += b.w + 16
d.note(20, 950, 960, ['Solo un ModeloIA por tipo puede estar ACTIVO. Si las métricas no alcanzan el mínimo (F1 ≥ 0,70 y MAE ≤ 3 días; top-5 ≥ 0,60 y',
    'MAPE ≤ 25 %; exactitud ≥ 0,80) el modelo queda RECHAZADO y sigue el anterior (IA-006). Riesgo: ALTO ≥ 70 %, MEDIO 40-69 %, BAJO < 40 %.',
    'Cada predicción o sugerencia guarda la versión del modelo que la generó (IA-015). Los modelos corren en el servicio Python (sgbh-ia).'])
print(d.render('img/c8.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
