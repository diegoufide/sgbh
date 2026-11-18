package cr.sgsoluciones506.businesshub.bitacora;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Marca un método de servicio cuya ejecución debe quedar en la bitácora (RNF-004).
 * El aspecto que la procesa escribe en la tabla bitacora dentro de la misma transacción.
 */
@Documented
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Auditable {

    /** Tabla afectada, por ejemplo "cotizacion". */
    String tabla();

    /** Operación registrada, por ejemplo "APROBAR". */
    String operacion();
}
