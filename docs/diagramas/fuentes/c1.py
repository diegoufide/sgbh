from uml import Diagram
d = Diagram()
ea = d.cls('EntidadAuditable', 300, 20, ['#id : Long', '#fechaCreacion : LocalDateTime', '#creadoPor : String',
    '#fechaModificacion : LocalDateTime', '#modificadoPor : String'], ['+getId() : Long', '+esNuevo() : boolean'],
    stereo='abstract', abstract=True)
d.note(600, 30, 340, ['Las entidades de negocio de todos los', 'paquetes heredan de EntidadAuditable', '(id y datos de auditoría). Bitacora y los',
    'registros de uso de la IA no heredan:', 'solo admiten inserción (RNF-004).'])
us = d.cls('Usuario', 270, 290, ['-nombre : String', '-correo : String', '-passwordHash : String', '-activo : boolean',
    '-intentosFallidos : int', '-bloqueadoHasta : LocalDateTime', '-ultimoAcceso : LocalDateTime'],
    ['+registrarIntentoFallido() : void', '+reiniciarIntentos() : void', '+estaBloqueado() : boolean', '+inactivar() : void'])
ro = d.cls('Rol', 545, 290, ['-nombre : NombreRol', '-descripcion : String'],
    ['+tienePermiso(codigo : String) : boolean', '+asignarPermiso(p : Permiso) : void', '+quitarPermiso(p : Permiso) : void'])
pe = d.cls('Permiso', 852, 290, ['-codigo : String', '-modulo : String', '-descripcion : String'], [])
no = d.cls('Notificacion', 10, 290, ['-tipo : TipoNotificacion', '-mensaje : String', '-enlace : String', '-leida : boolean',
    '-abierta : boolean', '-fechaHora : LocalDateTime'], ['+marcarLeida() : void', '+cerrar() : void'])
nr = d.enum('NombreRol', 566.5, 500, ['ADMINISTRADOR', 'SERVICIO_AL_CLIENTE', 'DISENADOR', 'FABRICANTE', 'SERVICIOS_PROFESIONALES'])
tk = d.cls('TokenRecuperacion', 200, 600, ['-token : String', '-expiraEn : LocalDateTime', '-usado : boolean'],
    ['+esValido(ahora : LocalDateTime) : boolean'])
bi = d.cls('Bitacora', 20, 770, ['-idBitacora : Long', '-fechaHora : LocalDateTime', '-usuario : String', '-rol : String',
    '-modulo : String', '-tabla : String', '-idRegistro : String', '-operacion : OperacionBitacora', '-valorAnterior : String (JSON)',
    '-valorNuevo : String (JSON)', '-motivo : String', '-detalle : String', '-direccionIp : String'],
    ['_+crear(datos : RegistroAuditoria) : Bitacora'], stereo='solo inserción')
ob = d.enum('OperacionBitacora', 400, 770, ['CREAR', 'ACTUALIZAR', 'ELIMINAR', 'INACTIVAR', 'CERRAR', 'REABRIR', 'ACCESO_DENEGADO',
    'INICIO_SESION', 'GENERAR_CONJUNTO', 'ENTRENAR', 'ACTIVAR', 'REVERTIR', 'CONFIGURAR'])
d.note(600, 800, 340, ['USUARIO y ROL se guardan como texto para', 'que el registro no cambie si después se', 'modifica el usuario. La base de datos solo',
    'permite INSERT en BITACORA; si la escritura', 'falla, la transacción completa se revierte.'])
bus = 250
tx = ea.x + ea.w / 2
for c in (no, us, ro, pe):
    x0 = c.x + c.w / 2
    d.rel(c, 'T', ea, 'B', 'inh', via=[(x0, bus), (tx, bus)])
d.rel(us, 'R', ro, 'L', 'assoc', ma='0..*', mb='1', label='tiene', ta=0.2, straight=True)
d.rel(ro, 'R', pe, 'L', 'assoc', ma='0..*', mb='1..*', label='incluye', ta=0.3, straight=True)
d.rel(us, 'B', tk, 'T', 'comp', ma='1', mb='0..*', label='solicita', ta=0.3, straight=True, label_side='right')
d.rel(no, 'R', us, 'L', 'assoc', ma='0..*', mb='1', label='destinatario', ta=0.3, straight=True)
d.rel(ro, 'B', nr, 'T', 'dep', ta=0.5, label='«use»', straight=True)
d.rel(bi, 'R', ob, 'L', 'dep', ta=0.3, label='«use»', straight=True)
print(d.render('img/c1.png'))
