from uml import Diagram
d = Diagram()
sol = d.ref('Solicitud', 40, 20, stereo='ver diagrama de clientes', w=180)
cli = d.ref('Cliente', 260, 20, stereo='ver diagrama de clientes', w=180)
cot = d.cls('Cotizacion', 40, 130, ['-numeroCotizacion : String', '-version : int', '-descripcionTrabajo : String',
    '-subtotal : BigDecimal', '-descuento : BigDecimal', '-iva : BigDecimal', '-total : BigDecimal', '-estado : EstadoCotizacion',
    '-fechaAprobacion : LocalDateTime', '-fechaVencimiento : LocalDate', '-decisionCliente : DecisionCliente',
    '-motivoRechazo : MotivoRechazo', '_+TASA_IVA : BigDecimal = 0.13 {readOnly}', '_+DIAS_VIGENCIA : int = 15 {readOnly}'],
    ['+agregarLinea(e : ElementoCatalogo, cantidad : BigDecimal) : void', '+quitarLinea(idLinea : Long) : void',
     '+calcularTotales() : void', '+aprobar(u : Usuario) : void', '+registrarDecision(d : DecisionCliente, m : MotivoRechazo) : void',
     '+crearNuevaVersion() : Cotizacion', '+vencer(hoy : LocalDate) : boolean', '+esEditable() : boolean'])
det = d.cls('CotizacionDetalle', 640, 130, ['-cantidad : BigDecimal', '-precioUnitario : BigDecimal', '-subtotalLinea : BigDecimal'],
    ['+calcularSubtotal() : BigDecimal', '+actualizarPrecio(nuevo : BigDecimal) : void'])
ele = d.cls('ElementoCatalogo', 640, 400, ['-nombre : String', '-tipo : TipoCatalogo', '-unidad : String', '-precioUnitario : BigDecimal',
    '-estado : EstadoRegistro'], ['+cambiarPrecio(nuevo : BigDecimal) : HistorialPrecio', '+inactivar() : void', '+estaEnUso() : boolean'])
his = d.cls('HistorialPrecio', 640, 700, ['-precioAnterior : BigDecimal', '-precioNuevo : BigDecimal', '-fechaHora : LocalDateTime'], [])
mat = d.ref('Material', 400, 720, stereo='ver diagrama de inventario', w=190)
y = 840
xs = 40
for name, lits in [('TipoCatalogo', ['SERVICIO', 'MATERIAL']),
                   ('EstadoCotizacion', ['BORRADOR', 'APROBADA_PARA_ENVIO', 'ACEPTADA', 'RECHAZADA', 'VENCIDA', 'REEMPLAZADA']),
                   ('DecisionCliente', ['ACEPTADA', 'RECHAZADA']),
                   ('MotivoRechazo', ['PRECIO', 'TIEMPO_ENTREGA', 'DISENO', 'OTRO'])]:
    b = d.enum(name, xs, y, lits)
    xs += b.w + 30
d.note(xs, y, 1000 - xs - 10, ['IVA del 13 % y vigencia de', '15 días (RNF-012, COT-002).', 'Montos en colones (₡),', 'redondeados a 2 decimales.'])
d.rel(cot, 'T', sol, 'B', 'assoc', ma='0..*', mb='1', label='responde a', ta=0.25, straight=True)
d.rel(cot, 'T', cli, 'B', 'assoc', ma='0..*', mb='1', label='para', ta=0.6, straight=True)
d.rel(cot, 'R', det, 'L', 'comp', ma='1', mb='0..*', label='contiene', ta=0.08, straight=True)
d.rel(det, 'B', ele, 'T', 'assoc', ma='0..*', mb='1', label='cotiza', ta=0.3, straight=True)
d.rel(ele, 'B', his, 'T', 'comp', ma='1', mb='0..*', label='registra', ta=0.3, straight=True)
d.rel(ele, 'L', mat, 'T', 'assoc', ma='0..*', mb='0..1', label='corresponde a', ta=0.75)
by = ele.y + ele.h + 34
d.rel(ele, 'B', ele, 'B', 'assoc', ma='0..*', mb='0..1', ta=0.72, tb=0.92, label='reemplazo',
      via=[(ele.x + ele.w * 0.72, by), (ele.x + ele.w * 0.92, by)], label_side='below')
cy = cot.y + cot.h + 34
d.rel(cot, 'B', cot, 'B', 'assoc', ma='0..1', mb='0..1', ta=0.35, tb=0.6, label='versión anterior',
      via=[(cot.x + cot.w * 0.35, cy), (cot.x + cot.w * 0.6, cy)], label_side='below')
print(d.render('img/c3.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
