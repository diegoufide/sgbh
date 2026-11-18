from uml import Diagram
d = Diagram()
pry = d.ref('Proyecto', 20, 20, stereo='ver diagrama de proyectos', w=200)
usr = d.ref('Usuario', 640, 20, stereo='ver diagrama de seguridad', w=190)
op = d.cls('OrdenProduccion', 20, 140, ['-numeroOrden : String', '-disenoFinal : String', '-especificaciones : String',
    '-estado : EstadoOrden', '-etapaProduccion : EtapaProduccion', '-materialEnEspera : boolean'],
    ['+asignarResponsables(fab : Usuario, inst : Usuario) : void', '+avanzar(e : EtapaProduccion, comentario : String) : AvanceProduccion',
     '+ponerEnEsperaDeMaterial() : void', '+liberarMaterial() : void', '+estaLista() : boolean'])
av = d.cls('AvanceProduccion', 640, 230, ['-etapa : EtapaProduccion', '-comentario : String', '-fotoAvance : String',
    '-fechaHora : LocalDateTime'], [])
en = d.cls('Entrega', 20, 520, ['-tipoEntrega : TipoEntrega', '-fechaProgramada : LocalDate', '-hora : LocalTime', '-direccion : String',
    '-motivoReprogramacion : String', '-fechaEntregaReal : LocalDate', '-recibidoPor : String', '-fotoEvidencia : String',
    '-diasAtraso : int', '-conIncidencia : boolean', '-descripcionIncidencia : String'],
    ['+programar(tipo : TipoEntrega, fecha : LocalDate, hora : LocalTime) : void', '+reprogramar(fecha : LocalDate, motivo : String) : void',
     '+registrarEntrega(fecha : LocalDate, recibidoPor : String, foto : String) : void', '+calcularDiasAtraso() : int'])
d.rel(op, 'T', pry, 'B', 'assoc', ma='0..1', mb='1', label='produce', ta=0.2, straight=True)
d.rel(op, 'R', usr, 'B', 'assoc', ma='0..*', mb='1', label='fabricante', ta=0.08, tb=0.25, label_t=0.6)
d.rel(op, 'R', usr, 'B', 'assoc', ma='0..*', mb='0..1', label='instalador', ta=0.2, tb=0.75, label_t=0.45)
d.rel(op, 'R', av, 'L', 'comp', ma='1', mb='0..*', label='registra', ta=0.45, straight=True)
d.rel(op, 'B', en, 'T', 'comp', ma='1', mb='0..1', label='se entrega mediante', ta=0.3, straight=True)
y = 520
xs = 640
b1 = d.enum('EstadoOrden', 640, y, ['EN_COLA', 'EN_ESPERA_DE_MATERIAL', 'EN_PRODUCCION', 'ENTREGADO'])
b2 = d.enum('EtapaProduccion', 640, y + 140, ['IMPRESION', 'CORTE', 'ARMADO', 'ACABADOS', 'LISTO'])
b3 = d.enum('TipoEntrega', 820, y + 140, ['RETIRO_TALLER', 'INSTALACION'])
d.note(640, y + 310, 340, ['Número OP-AAAA-0001 (PRD-001). Si falta', 'material la orden queda EN_ESPERA_DE_', 'MATERIAL; DIAS_ATRASO se calcula si la',
    'entrega real supera la programada (PRD-005).'])
print(d.render('img/c6.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
