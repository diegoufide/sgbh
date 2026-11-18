from uml import Diagram
d = Diagram()
pry = d.cls('Proyecto', 20, 130, ['-codigoProyecto : String', '-nombreProyecto : String', '-tipoServicio : String',
    '-fechaInicio : LocalDate', '-fechaEntrega : LocalDate', '-estado : EstadoProyecto', '-fechaCierre : LocalDate',
    '-observacionCierre : String', '-motivoReapertura : String'],
    ['+agregarTarea(t : Tarea) : void', '+asignarMaterial(m : Material, c : BigDecimal) : ProyectoMaterial', '+iniciar() : void',
     '+cerrar(fecha : LocalDate, obs : String) : void', '+reabrir(motivo : String) : void', '+tareasPendientes() : List<Tarea>'])
cli = d.ref('Cliente', 20, 20, stereo='ver diagrama de clientes', w=160)
sol = d.ref('Solicitud', 200, 20, stereo='ver diagrama de clientes', w=160)
cot = d.ref('Cotizacion', 380, 20, stereo='ver cotizaciones', w=130)
tar = d.cls('Tarea', 560, 130, ['-etapa : String', '-nombre : String', '-descripcion : String', '-prioridad : Prioridad',
    '-fechaLimite : LocalDate', '-cantidadReprogramaciones : int', '-estado : EstadoTarea', '-porcentajeAvance : int',
    '-fechaCompletada : LocalDateTime', '-atrasada : boolean', '-nivelRiesgo : NivelRiesgo'],
    ['+asignar(u : Usuario) : void', '+reprogramar(f : LocalDate, m : MotivoCambioFecha) : void',
     '+registrarAvance(pct : int, comentario : String) : HistorialTarea', '+estaVencida(hoy : LocalDate) : boolean'])
usr = d.ref('Usuario', 780, 20, stereo='ver diagrama de seguridad', w=180)
his = d.cls('HistorialTarea', 600, 520, ['-tipoCambio : TipoCambioTarea', '-valorAnterior : String', '-valorNuevo : String',
    '-comentario : String', '-fechaHora : LocalDateTime'], [])
pm = d.cls('ProyectoMaterial', 20, 520, ['-cantidad : BigDecimal'], ['+sumarCantidad(c : BigDecimal) : void'])
mat = d.ref('Material', 330, 538, stereo='ver diagrama de inventario', w=185)
d.rel(pry, 'T', cli, 'B', 'assoc', ma='0..*', mb='1', label='de', ta=0.15, straight=True)
d.rel(pry, 'T', sol, 'B', 'assoc', ma='0..1', mb='1', label='origina', ta=0.6, straight=True)
d.rel(pry, 'T', cot, 'B', 'assoc', ma='0..1', mb='1', label='aceptada', ta=0.97, straight=True, label_side='left')
d.rel(pry, 'R', tar, 'L', 'comp', ma='1', mb='0..*', label='planifica', ta=0.1, straight=True)
d.rel(tar, 'T', usr, 'B', 'assoc', ma='0..*', mb='0..1', label='responsable', ta=0.75, straight=True)
d.rel(tar, 'B', his, 'T', 'comp', ma='1', mb='0..*', label='historial', ta=0.3, straight=True)
d.rel(pry, 'B', pm, 'T', 'comp', ma='1', mb='0..*', label='recursos', ta=0.2, straight=True)
d.rel(pm, 'R', mat, 'L', 'assoc', ma='0..*', mb='1', label='usa', ta=0.5, straight=True)
y = 700
xs = 20
for name, lits in [('EstadoProyecto', ['PLANIFICACION', 'EN_EJECUCION', 'CERRADO']),
                   ('EstadoTarea', ['PENDIENTE', 'EN_PROCESO', 'COMPLETADA', 'CANCELADA']),
                   ('Prioridad', ['ALTA', 'MEDIA', 'BAJA']),
                   ('MotivoCambioFecha', ['CAMBIO_CLIENTE', 'FALTA_MATERIAL', 'SOBRECARGA', 'OTRO']),
                   ('TipoCambioTarea', ['AVANCE', 'REPROGRAMACION', 'REASIGNACION', 'CAMBIO_ESTADO'])]:
    b = d.enum(name, xs, y, lits)
    xs += b.w + 18
d.note(20, 840, 600, ['ATRASADA = FECHA_COMPLETADA > FECHA_LIMITE se calcula al completar la tarea', '(PRO-005) y es la etiqueta del modelo de atrasos (IA-002). NIVEL_RIESGO lo',
    'actualiza el análisis diario de la IA (IA-008); ver diagrama de IA.'])
print(d.render('img/c5.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
