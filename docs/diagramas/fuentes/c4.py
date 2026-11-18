from uml import Diagram
d = Diagram()
mat = d.cls('Material', 20, 20, ['-codigo : String', '-nombre : String', '-unidadMedida : UnidadMedida', '-existencia : BigDecimal {readOnly}',
    '-stockMinimo : BigDecimal', '-estado : EstadoRegistro'],
    ['+aplicar(m : MovimientoInventario) : void', '+puedeDescontar(cantidad : BigDecimal) : boolean', '+estaBajoMinimo() : boolean',
     '+inactivar() : void'])
mov = d.cls('MovimientoInventario', 520, 20, ['-tipoMovimiento : TipoMovimiento', '-cantidad : BigDecimal', '-fecha : LocalDate',
    '-numeroFactura : String', '-motivo : String', '-existenciaResultante : BigDecimal'],
    ['+anular(motivo : String) : MovimientoInventario', '+signo() : int'])
ale = d.cls('AlertaInventario', 20, 360, ['-existencia : BigDecimal', '-stockMinimo : BigDecimal', '-fechaHora : LocalDateTime',
    '-abierta : boolean'], ['+actualizarExistencia(e : BigDecimal) : void', '+cerrar() : void'])
pro = d.cls('Proveedor', 330, 360, ['-nombre : String', '-cedulaJuridica : String', '-telefono : String', '-correo : String',
    '-estado : EstadoRegistro'], ['+inactivar() : void'])
pry = d.ref('Proyecto', 720, 380, stereo='ver diagrama de proyectos', w=205)
d.rel(mov, 'L', mat, 'R', 'assoc', ma='0..*', mb='1', label='afecta', ta=0.3, straight=True)
d.rel(ale, 'T', mat, 'B', 'assoc', ma='0..*', mb='1', label='sobre', ta=0.4, straight=True)
d.rel(mat, 'B', pro, 'T', 'line', ma='0..*', mb='0..*', label='suministra', ta=0.9, tb=0.5, via=[(20 + 312 * 0.9, 300), (411, 300)], label_pos=(356, 293))
d.rel(mov, 'B', pro, 'R', 'assoc', ma='0..*', mb='0..1', label='comprado a', ta=0.12, tb=0.3, label_side='right')
d.rel(mov, 'B', pry, 'T', 'assoc', ma='0..*', mb='0..1', label='destinado a', ta=0.8, straight=True)
d.rel(mov, 'R', mov, 'R', 'assoc', ma='0..1', mb='0..1', ta=0.3, tb=0.6, label='anula',
      via=[(mov.x + mov.w + 34, mov.y + mov.h * 0.3), (mov.x + mov.w + 34, mov.y + mov.h * 0.6)], label_side='right')
y = 560
b1 = d.enum('UnidadMedida', 20, y, ['UNIDAD', 'METRO', 'METRO_CUADRADO', 'LITRO', 'ROLLO'])
b2 = d.enum('TipoMovimiento', 220, y, ['ENTRADA', 'SALIDA', 'DEVOLUCION', 'ANULACION'])
d.note(420, y, 520, ['La existencia no se edita a mano: solo cambia al aplicar un', 'MovimientoInventario (entrada, salida, devolución o anulación).',
    'No se aceptan cantidades en 0, negativas ni existencias', 'negativas (RNF-010). Una alerta abierta se actualiza en lugar', 'de crear otra (INV-005).'])
print(d.render('img/c4.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
