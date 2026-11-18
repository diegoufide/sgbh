from uml import Diagram
d = Diagram()
con = d.cls('ContactoCliente', 10, 20, ['-nombreContacto : String', '-puesto : String', '-telefono : String', '-correo : String',
    '-principal : boolean'], ['+marcarPrincipal() : void'])
cli = d.cls('Cliente', 260, 20, ['-nombre : String', '-tipoCliente : TipoCliente', '-identificacion : String', '-telefono : String',
    '-correo : String', '-direccion : String', '-estado : EstadoRegistro'],
    ['+actualizarDatos(form : ClienteForm) : void', '+inactivar() : void', '+activar() : void', '+tieneHistorial() : boolean',
     '+contactoPrincipal() : ContactoCliente'])
com = d.cls('Comunicacion', 680, 20, ['-canal : Canal', '-fechaHora : LocalDateTime', '-resumen : String', '-categoria : CategoriaMensaje',
    '-categoriaSugerida : CategoriaMensaje', '-confianza : BigDecimal', '-categoriaConfirmada : boolean'],
    ['+confirmarCategoria(c : CategoriaMensaje) : void', '+asociarProyecto(p : Proyecto) : void'])
usr = d.ref('Usuario', 10, 420, stereo='ver diagrama de seguridad', w=172)
sol = d.cls('Solicitud', 260, 360, ['-numeroSolicitud : String', '-canal : Canal', '-tipoServicio : String', '-descripcion : String',
    '-fechaRegistro : LocalDateTime', '-fechaCompromiso : LocalDate', '-estado : EstadoSolicitud', '-motivoCancelacion : String'],
    ['+asignarResponsable(u : Usuario) : void', '+cambiarEstado(nuevo : EstadoSolicitud) : void', '+cancelar(motivo : String) : void',
     '+puedeConvertirseEnProyecto() : boolean'])
sc = d.cls('SolicitudCambio', 680, 340, ['-descripcionCambio : String', '-afectaCotizacion : boolean', '-afectaFecha : boolean',
    '-nuevaFechaEntrega : LocalDate', '-estadoCambio : EstadoCambio', '-motivo : String'],
    ['+aprobar(u : Usuario) : void', '+rechazar(motivo : String) : void'])
pry = d.ref('Proyecto', 680, 640, stereo='ver diagrama de proyectos', w=208)
arc = d.cls('ArchivoAdjunto', 120, 720, ['-nombreArchivo : String', '-rutaArchivo : String', '-tipoMime : String', '-tamanoBytes : long'],
    ['+esFormatoPermitido() : boolean'])
obs = d.cls('ObservacionSolicitud', 420, 720, ['-observacion : String', '-fechaHora : LocalDateTime'], [])
y = 900
xs = 10
for name, lits in [('TipoCliente', ['PERSONA', 'EMPRESA']), ('EstadoRegistro', ['ACTIVO', 'INACTIVO']),
                   ('Canal', ['WHATSAPP', 'LLAMADA', 'CORREO', 'REDES_SOCIALES', 'PRESENCIAL']),
                   ('EstadoSolicitud', ['NUEVA', 'EN_COTIZACION', 'APROBADA', 'EN_PROYECTO', 'FINALIZADA', 'CANCELADA']),
                   ('CategoriaMensaje', ['CONSULTA', 'SOLICITUD_CAMBIO', 'QUEJA', 'APROBACION', 'PAGO']),
                   ('EstadoCambio', ['PENDIENTE', 'APROBADO', 'RECHAZADO'])]:
    b = d.enum(name, xs, y, lits)
    xs += b.w + 22
d.note(640, 760, 330, ['Los enumerados son tipos de atributo;', 'se guardan como texto (VARCHAR) en la', 'base de datos.'])
d.rel(cli, 'L', con, 'R', 'comp', ma='1', mb='0..*', label='tiene', ta=0.35, straight=True)
d.rel(sol, 'T', cli, 'B', 'assoc', ma='0..*', mb='1', label='realizada por', ta=0.3, straight=True)
d.rel(com, 'L', cli, 'R', 'assoc', ma='0..*', mb='1', label='con', ta=0.4, straight=True)
d.rel(com, 'R', pry, 'R', 'assoc', ma='0..*', mb='0..1', label='asociada a', ta=0.5, via=[(1010, 20 + com.h * 0.5), (1010, 661)], label_side='left', label_t=0.62)
d.rel(sc, 'B', pry, 'T', 'assoc', ma='0..*', mb='1', label='modifica', ta=0.4, straight=True)
d.rel(sc, 'T', com, 'B', 'assoc', ma='0..1', mb='0..1', label='originada en', ta=0.4, straight=True)
d.rel(sol, 'L', usr, 'R', 'assoc', ma='0..*', mb='0..1', label='responsable', ta=0.25, straight=True)
d.rel(sol, 'B', arc, 'T', 'comp', ma='1', mb='0..5', label='adjunta', ta=0.2, tb=0.5)
d.rel(sol, 'B', obs, 'T', 'comp', ma='1', mb='0..*', label='registra', ta=0.75, tb=0.4)
print(d.render('img/c2.png'))
