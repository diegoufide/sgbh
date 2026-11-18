package cr.sgsoluciones506.businesshub.comun.model;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import java.time.LocalDateTime;

/**
 * Superclase de las entidades del negocio: fechas y usuarios de creación y modificación.
 */
@MappedSuperclass
public abstract class EntidadAuditable {

    @Column(name = "fecha_creacion", nullable = false, updatable = false)
    protected LocalDateTime fechaCreacion;

    @Column(name = "creado_por", length = 60, updatable = false)
    protected String creadoPor;

    @Column(name = "fecha_modificacion")
    protected LocalDateTime fechaModificacion;

    @Column(name = "modificado_por", length = 60)
    protected String modificadoPor;

    @PrePersist
    protected void alCrear() {
        fechaCreacion = LocalDateTime.now();
    }

    @PreUpdate
    protected void alModificar() {
        fechaModificacion = LocalDateTime.now();
    }

    public LocalDateTime getFechaCreacion() {
        return fechaCreacion;
    }

    public String getCreadoPor() {
        return creadoPor;
    }

    public LocalDateTime getFechaModificacion() {
        return fechaModificacion;
    }

    public String getModificadoPor() {
        return modificadoPor;
    }
}
