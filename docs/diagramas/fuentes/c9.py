from uml import Diagram
d = Diagram()
frm = d.cls('CotizacionForm', 20, 20, ['-idSolicitud : Long', '-descripcionTrabajo : String', '-lineas : List<LineaForm>',
    '-descuento : BigDecimal'], [], stereo='DTO')
ctl = d.cls('CotizacionController', 300, 20, ['-cotizacionService : CotizacionService'],
    ['+listar(filtro : FiltroCotizacion, model : Model) : String', '+guardar(form : CotizacionForm, br : BindingResult) : String',
     '+aprobar(id : Long) : String', '+descargarPdf(id : Long) : ResponseEntity<byte[]>'], stereo='Controller')
sug = d.cls('SugerenciaCotizacionController', 700, 20, ['-iaClient : IaServiceClient', '-cotizacionService : CotizacionService'],
    ['+sugerir(id : Long) : List<SugerenciaDTO>'], stereo='RestController · paquete ia')
srv = d.cls('CotizacionService', 300, 250, [], ['+crear(form : CotizacionForm) : Cotizacion', '+aprobar(id : Long) : Cotizacion',
    '+registrarDecision(id : Long, d : DecisionCliente) : void', '+generarPdf(id : Long) : byte[]', '+vencerCotizaciones() : int'], stereo='interface')
ia = d.cls('IaServiceClient', 710, 250, ['-restClient : RestClient', '-timeout : Duration = 60 s'],
    ['+sugerirCotizacion(req) : SugerenciaResponse'], stereo='Component')
imp = d.cls('CotizacionServiceImpl', 300, 480, ['-cotizacionRepository : CotizacionRepository', '-catalogoRepository : CatalogoRepository',
    '-pdfGenerator : PdfGenerator', '-bitacoraService : BitacoraService'],
    ['+crear(form : CotizacionForm) : Cotizacion', '+aprobar(id : Long) : Cotizacion', '+vencerCotizaciones() : int'], stereo='Service')
pdf = d.cls('PdfGenerator', 20, 500, [], ['+generar(c : Cotizacion) : byte[]'], stereo='Component')
bit = d.cls('BitacoraService', 690, 500, [], ['+registrar(r : RegistroAuditoria) : void'], stereo='Service · paquete bitacora')
rep = d.cls('CotizacionRepository', 330, 760, [], ['+findByEstado(e : EstadoCotizacion) : List<Cotizacion>',
    '+findVencibles(hoy : LocalDate) : List<Cotizacion>'], stereo='interface')
cat = d.cls('CatalogoRepository', 20, 760, [], ['+findActivos() : List<ElementoCatalogo>'], stereo='interface')
jpa = d.ref('JpaRepository<Cotizacion, Long>', 720, 795, stereo='interface · Spring Data', w=250)
ent = d.ref('Cotizacion', 400, 940, stereo='Entity', w=150)
d.rel(ctl, 'L', frm, 'R', 'dep', ta=0.5, straight=True, label='«use»')
d.rel(ctl, 'B', srv, 'T', 'assoc', mb='1', ta=0.5, straight=True)
d.rel(sug, 'B', ia, 'T', 'assoc', mb='1', ta=0.75, straight=True)
d.rel(sug, 'L', srv, 'R', 'assoc', mb='1', ta=0.85, tb=0.25, via=[(682, 20 + 0.85 * sug.h), (682, 250 + 0.25 * srv.h)])
d.rel(imp, 'T', srv, 'B', 'real', ta=0.5, straight=True)
d.rel(imp, 'L', pdf, 'R', 'assoc', mb='1', ta=0.3, straight=True)
d.rel(imp, 'R', bit, 'L', 'assoc', mb='1', ta=0.3, straight=True)
d.rel(imp, 'B', rep, 'T', 'assoc', mb='1', ta=0.5, straight=True)
d.rel(imp, 'B', cat, 'T', 'assoc', mb='1', ta=0.1, tb=0.75)
d.rel(rep, 'R', jpa, 'L', 'inh', ta=0.5, straight=True)
d.rel(rep, 'B', ent, 'T', 'dep', ta=0.3, straight=True, label='«use»')
d.note(620, 930, 380, ['Capas: Controller → Service → Repository.', '@Transactional en la implementación del servicio;',
    'la bitácora se escribe en la misma transacción.', 'El paquete ia depende de cotizacion, nunca al revés.'])
print(d.render('img/c9.png'))
for n, b in d.boxes.items(): print(n, b.x, b.y, round(b.w), b.h)
