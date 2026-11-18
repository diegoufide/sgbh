-- V1: tablas base de seguridad y bitácora (M8 Usuarios y seguridad)
-- Convenciones: tablas en singular snake_case, llave primaria id_<tabla>.

CREATE TABLE rol (
    id_rol         BIGSERIAL    CONSTRAINT pk_rol PRIMARY KEY,
    nombre         VARCHAR(40)  NOT NULL CONSTRAINT uq_rol_nombre UNIQUE,
    descripcion    VARCHAR(200),
    CONSTRAINT ck_rol_nombre CHECK (nombre IN ('ADMINISTRADOR', 'SERVICIO_AL_CLIENTE', 'DISENADOR',
                                               'FABRICANTE', 'SERVICIOS_PROFESIONALES'))
);

CREATE TABLE permiso (
    id_permiso     BIGSERIAL    CONSTRAINT pk_permiso PRIMARY KEY,
    codigo         VARCHAR(60)  NOT NULL CONSTRAINT uq_permiso_codigo UNIQUE,
    modulo         VARCHAR(40)  NOT NULL,
    descripcion    VARCHAR(200)
);

CREATE TABLE rol_permiso (
    id_rol         BIGINT NOT NULL CONSTRAINT fk_rol_permiso_rol REFERENCES rol (id_rol),
    id_permiso     BIGINT NOT NULL CONSTRAINT fk_rol_permiso_permiso REFERENCES permiso (id_permiso),
    CONSTRAINT pk_rol_permiso PRIMARY KEY (id_rol, id_permiso)
);

CREATE TABLE usuario (
    id_usuario           BIGSERIAL    CONSTRAINT pk_usuario PRIMARY KEY,
    nombre               VARCHAR(120) NOT NULL,
    correo               VARCHAR(120) NOT NULL CONSTRAINT uq_usuario_correo UNIQUE,
    password_hash        VARCHAR(100) NOT NULL,
    id_rol               BIGINT       NOT NULL CONSTRAINT fk_usuario_rol REFERENCES rol (id_rol),
    activo               BOOLEAN      NOT NULL DEFAULT TRUE,
    intentos_fallidos    INTEGER      NOT NULL DEFAULT 0,
    bloqueado_hasta      TIMESTAMP,
    ultimo_acceso        TIMESTAMP,
    fecha_creacion       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    creado_por           VARCHAR(60),
    fecha_modificacion   TIMESTAMP,
    modificado_por       VARCHAR(60),
    CONSTRAINT ck_usuario_intentos CHECK (intentos_fallidos >= 0)
);

CREATE TABLE bitacora (
    id_bitacora      BIGSERIAL    CONSTRAINT pk_bitacora PRIMARY KEY,
    fecha_hora       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario       BIGINT       CONSTRAINT fk_bitacora_usuario REFERENCES usuario (id_usuario),
    rol              VARCHAR(40),
    modulo           VARCHAR(40)  NOT NULL,
    tabla            VARCHAR(60)  NOT NULL,
    id_registro      BIGINT,
    operacion        VARCHAR(30)  NOT NULL,
    valor_anterior   JSONB,
    valor_nuevo      JSONB,
    motivo           VARCHAR(300),
    detalle          VARCHAR(500),
    direccion_ip     VARCHAR(45)
);

CREATE INDEX ix_usuario_id_rol ON usuario (id_rol);
CREATE INDEX ix_bitacora_fecha_hora ON bitacora (fecha_hora);
CREATE INDEX ix_bitacora_tabla_id_registro ON bitacora (tabla, id_registro);

-- La bitácora es de solo inserción (RNF-004). En producción, el rol de la aplicación
-- solo recibe INSERT y SELECT sobre esta tabla:
--   REVOKE UPDATE, DELETE, TRUNCATE ON sgbh.bitacora FROM sgbh_app;
