-- V2: los cinco roles del sistema (AN02, hoja «Guía y roles»)
INSERT INTO rol (nombre, descripcion) VALUES
    ('ADMINISTRADOR', 'Configura el sistema, aprueba y es el único que administra la IA'),
    ('SERVICIO_AL_CLIENTE', 'Atiende clientes, solicitudes, cotizaciones y comunicaciones'),
    ('DISENADOR', 'Diseño, visualización de espacios y propuestas'),
    ('FABRICANTE', 'Producción, materiales e inventario'),
    ('SERVICIOS_PROFESIONALES', 'Colaborador externo: solo ve lo que se le asigna y nunca ve precios');
