-- ============================================================
-- Base de datos de Licitaciones del Sector Público de España
-- Fuente: Plataforma de Contratación del Sector Público
-- ============================================================

CREATE DATABASE licitaciones
    WITH ENCODING = 'UTF8'
         LC_COLLATE = 'es_ES.UTF-8'
         LC_CTYPE = 'es_ES.UTF-8'
         TEMPLATE = template0;

\c licitaciones

-- Extensión para generación de UUIDs si se necesita en el futuro
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Limpieza de la tabla antigua de usuario-superficie, ya no forma parte del modelo
DROP TABLE IF EXISTS usuario_superficie CASCADE;

-- ============================================================
-- Tabla principal de licitaciones
-- ============================================================
CREATE TABLE IF NOT EXISTS licitacion (

    -- === Identificación ===
    id_plataforma           TEXT        NOT NULL,   -- ID del entry Atom (URL sindicación), ej: https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/16559559
    expediente              TEXT,                   -- cbc:ContractFolderID, ej: EXP20.2025
    uuid_ted                TEXT,                   -- cbc:UUID schemeName="TED"
    link_detalle            TEXT,                   -- link href del entry Atom

    -- === Estado y fechas ===
    estado                  TEXT,                   -- cbc-place-ext:ContractFolderStatusCode (EV, ADJ, RES, etc.)
    updated_at              TIMESTAMPTZ NOT NULL,   -- <updated> del entry Atom (fecha de última actualización en la fuente)
    anulada                 BOOLEAN     NOT NULL DEFAULT FALSE,  -- true si viene como at:deleted-entry
    fecha_anulacion         TIMESTAMPTZ,            -- @when del deleted-entry

    -- === Datos del proyecto/contrato ===
    titulo                  TEXT,                   -- <title> del entry / cac:ProcurementProject > cbc:Name
    resumen                 TEXT,                   -- <summary> del entry
    tipo_contrato           TEXT,                   -- cbc:TypeCode (1=Suministro, 2=Servicios, 3=Obras, etc.)
    subtipo_contrato        TEXT,                   -- cbc:SubTypeCode
    contrato_mixto          BOOLEAN,                -- cbc:MixContractIndicator
    cpv_codes               TEXT[],                 -- Todos los códigos CPV (proyecto principal + lotes)

    -- === Importes del presupuesto ===
    importe_total           NUMERIC(18,2),          -- cac:BudgetAmount > cbc:TotalAmount
    importe_sin_impuestos   NUMERIC(18,2),          -- cac:BudgetAmount > cbc:TaxExclusiveAmount
    importe_estimado        NUMERIC(18,2),          -- cac:BudgetAmount > cbc:EstimatedOverallContractAmount
    moneda                  TEXT DEFAULT 'EUR',     -- @currencyID

    -- === Ubicación del contrato ===
    ubicacion_nuts          TEXT,                   -- cbc:CountrySubentityCode (código NUTS)
    ubicacion_comunidad     TEXT,                   -- cbc:CountrySubentity
    ubicacion_ciudad        TEXT,                   -- cac:Address > cbc:CityName
    ubicacion_cp            TEXT,                   -- cac:Address > cbc:PostalZone
    ubicacion_pais          TEXT DEFAULT 'ES',      -- cac:Country > cbc:IdentificationCode

    -- === Plazos del proyecto ===
    fecha_inicio_ejecucion  DATE,                   -- cac:PlannedPeriod > cbc:StartDate
    fecha_fin_ejecucion     DATE,                   -- cac:PlannedPeriod > cbc:EndDate

    -- === Órgano de contratación ===
    organo_contratacion     TEXT,                   -- cac:Party > cac:PartyName > cbc:Name
    organo_nif              TEXT,                   -- cac:PartyIdentification > cbc:ID schemeName="NIF"
    organo_id_plataforma    TEXT,                   -- cac:PartyIdentification > cbc:ID schemeName="ID_PLATAFORMA"
    organo_web              TEXT,                   -- cbc:WebsiteURI
    organo_email            TEXT,                   -- cac:Contact > cbc:ElectronicMail
    organo_telefono         TEXT,                   -- cac:Contact > cbc:Telephone
    organo_direccion        TEXT,                   -- cac:AddressLine > cbc:Line
    organo_ciudad           TEXT,                   -- cac:PostalAddress > cbc:CityName
    organo_cp               TEXT,                   -- cac:PostalAddress > cbc:PostalZone
    organo_perfil_url       TEXT,                   -- cbc:BuyerProfileURIID
    tipo_organo             TEXT,                   -- cbc:ContractingPartyTypeCode
    actividad_organo        TEXT,                   -- cbc:ActivityCode

    -- === Procedimiento de licitación ===
    procedimiento           TEXT,                   -- cac:TenderingProcess > cbc:ProcedureCode
    urgencia                TEXT,                   -- cbc:UrgencyCode
    forma_presentacion      TEXT,                   -- cbc:PartPresentationCode
    sistema_contratacion    TEXT,                   -- cbc:ContractingSystemCode
    metodo_envio            TEXT,                   -- cbc:SubmissionMethodCode
    sobre_umbral            BOOLEAN,                -- cbc:OverThresholdIndicator

    -- === Plazos de licitación ===
    fecha_limite_presentacion       TIMESTAMPTZ,    -- TenderSubmissionDeadlinePeriod > EndDate + EndTime
    fecha_limite_documentacion      TIMESTAMPTZ,    -- DocumentAvailabilityPeriod > EndDate + EndTime

    -- === Resultado de la licitación (si aplica) ===
    resultado_codigo        TEXT,                   -- TenderResult > cbc:ResultCode
    resultado_descripcion   TEXT,                   -- TenderResult > cbc:Description
    fecha_adjudicacion      DATE,                   -- TenderResult > cbc:AwardDate
    ofertas_recibidas       INTEGER,                -- TenderResult > cbc:ReceivedTenderQuantity
    ofertas_pymes           INTEGER,                -- TenderResult > cbc:SMEsReceivedTenderQuantity
    adjudicada_pyme         BOOLEAN,                -- TenderResult > cbc:SMEAwardedIndicator
    importe_oferta_menor    NUMERIC(18,2),          -- TenderResult > cbc:LowerTenderAmount
    importe_oferta_mayor    NUMERIC(18,2),          -- TenderResult > cbc:HigherTenderAmount

    -- === Adjudicatario ===
    adjudicatario_nombre    TEXT,                   -- WinningParty > PartyName > cbc:Name
    adjudicatario_nif       TEXT,                   -- WinningParty > PartyIdentification > cbc:ID
    adjudicatario_ciudad    TEXT,                   -- WinningParty > PhysicalLocation > Address > CityName
    adjudicatario_cp        TEXT,                   -- WinningParty > PhysicalLocation > Address > PostalZone

    -- === Contrato formalizado ===
    contrato_id             TEXT,                   -- TenderResult > Contract > cbc:ID
    contrato_fecha          DATE,                   -- TenderResult > Contract > cbc:IssueDate
    contrato_importe_sin_iva NUMERIC(18,2),         -- AwardedTenderedProject > TaxExclusiveAmount
    contrato_importe_total  NUMERIC(18,2),          -- AwardedTenderedProject > PayableAmount

    -- === Condiciones de la licitación ===
    financiacion_ue         TEXT,                   -- cbc:FundingProgramCode
    legislacion_nacional    TEXT,                   -- cbc:ProcurementNationalLegislationCode
    legislacion_referencia  TEXT,                   -- cac:ProcurementLegislationDocumentReference > cbc:ID
    idioma                  TEXT,                   -- cac:Language > cbc:ID
    subasta                 BOOLEAN,                -- AuctionTerms > AuctionConstraintIndicator

    -- === Jerarquía organizativa (ParentLocatedParty, hasta 6 niveles) ===
    jerarquia_org           TEXT[],                 -- Array con la cadena de ParentLocatedParty names

    -- === Metadatos de importación ===
    fichero_origen          TEXT,                   -- Nombre del fichero ATOM de donde se importó
    fecha_importacion       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_ultima_sync       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- === Datos XML originales para referencia ===
    entry_xml               TEXT,                   -- XML completo del entry por si se necesita reprocesar

    -- === Restricciones ===
    CONSTRAINT licitacion_pk PRIMARY KEY (id_plataforma)
);

-- ============================================================
-- Índices
-- ============================================================
CREATE INDEX idx_licitacion_expediente       ON licitacion (expediente);
CREATE INDEX idx_licitacion_estado           ON licitacion (estado);
CREATE INDEX idx_licitacion_updated_at       ON licitacion (updated_at);
CREATE INDEX idx_licitacion_organo_nif       ON licitacion (organo_nif);
CREATE INDEX idx_licitacion_cpv_codes    ON licitacion USING GIN (cpv_codes);
CREATE INDEX idx_licitacion_tipo_contrato    ON licitacion (tipo_contrato);
CREATE INDEX idx_licitacion_ubicacion_nuts   ON licitacion (ubicacion_nuts);
CREATE INDEX idx_licitacion_fecha_limite     ON licitacion (fecha_limite_presentacion);
CREATE INDEX idx_licitacion_adjudicatario    ON licitacion (adjudicatario_nif);
CREATE INDEX idx_licitacion_anulada          ON licitacion (anulada) WHERE anulada = TRUE;

-- Índice de texto completo para búsquedas en título y resumen
CREATE INDEX idx_licitacion_titulo_tsvector  ON licitacion USING GIN (to_tsvector('spanish', COALESCE(titulo, '')));
CREATE INDEX idx_licitacion_resumen_tsvector ON licitacion USING GIN (to_tsvector('spanish', COALESCE(resumen, '')));

-- ============================================================
-- Tabla de control de ficheros ya procesados
-- Evita reprocesar ficheros ATOM que ya han sido leídos
-- ============================================================
CREATE TABLE IF NOT EXISTS fichero_procesado (
    nombre_fichero      TEXT        NOT NULL,        -- Nombre del fichero ATOM (sin ruta)
    fecha_procesado     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    entries_totales     INTEGER,                     -- Total de entries en el fichero
    entries_filtradas   INTEGER,                     -- Entries que pasaron los filtros
    entries_insertadas  INTEGER,                     -- Entries efectivamente insertadas/actualizadas
    deleted_entries     INTEGER,                     -- deleted-entry encontradas
    anulaciones_aplicadas INTEGER,                   -- Anulaciones efectivamente aplicadas

    CONSTRAINT fichero_procesado_pk PRIMARY KEY (nombre_fichero)
);

COMMENT ON TABLE  fichero_procesado IS 'Registro de ficheros ATOM ya importados para evitar reprocesarlos';
COMMENT ON COLUMN fichero_procesado.nombre_fichero IS 'Nombre del fichero (basename), ej: licitacionesPerfilesContratanteCompleto3_20260327_202106.atom';

-- ============================================================
-- Tablas de gestión administrativa de usuarios
-- ============================================================
CREATE TABLE IF NOT EXISTS usuario (
    id                      TEXT        NOT NULL,
    nombre                  TEXT        NOT NULL,
    apellidos               TEXT        NOT NULL,
    email                   TEXT        NOT NULL,
    rol_principal           TEXT        NOT NULL,
    estado                  TEXT        NOT NULL,
    observaciones_internas   TEXT        NOT NULL DEFAULT '',
    fecha_alta              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ultimo_acceso           TIMESTAMPTZ,
    invitacion_pendiente     BOOLEAN     NOT NULL DEFAULT FALSE,

    CONSTRAINT usuario_pk PRIMARY KEY (id),
    CONSTRAINT usuario_email_uk UNIQUE (email),
    CONSTRAINT usuario_estado_ck CHECK (estado IN ('activo', 'inactivo', 'pendiente', 'bloqueado', 'baja logica')),
    CONSTRAINT usuario_nombre_ck CHECK (btrim(nombre) <> ''),
    CONSTRAINT usuario_apellidos_ck CHECK (btrim(apellidos) <> ''),
    CONSTRAINT usuario_email_ck CHECK (btrim(email) <> ''),
    CONSTRAINT usuario_rol_ck CHECK (btrim(rol_principal) <> '')
);

CREATE INDEX idx_usuario_estado ON usuario (estado);
CREATE INDEX idx_usuario_rol_principal ON usuario (rol_principal);
CREATE INDEX idx_usuario_email ON usuario (email);
CREATE INDEX idx_usuario_fecha_alta ON usuario (fecha_alta);

CREATE TABLE IF NOT EXISTS usuario_historial (
    id                      BIGSERIAL   NOT NULL,
    usuario_id              TEXT        NOT NULL,
    accion                  TEXT        NOT NULL,
    fecha                   TIMESTAMPTZ NOT NULL,
    detalle                 TEXT        NOT NULL,

    CONSTRAINT usuario_historial_pk PRIMARY KEY (id),
    CONSTRAINT usuario_historial_usuario_fk FOREIGN KEY (usuario_id) REFERENCES usuario (id) ON DELETE CASCADE,
    CONSTRAINT usuario_historial_uk UNIQUE (usuario_id, fecha, accion, detalle),
    CONSTRAINT usuario_historial_accion_ck CHECK (btrim(accion) <> ''),
    CONSTRAINT usuario_historial_detalle_ck CHECK (btrim(detalle) <> '')
);

CREATE INDEX idx_usuario_historial_usuario_fecha ON usuario_historial (usuario_id, fecha DESC, id DESC);

INSERT INTO usuario (id, nombre, apellidos, email, rol_principal, estado, observaciones_internas, fecha_alta, ultimo_acceso, invitacion_pendiente)
VALUES
    ('usr-001', 'Ana', 'Lopez', 'ana.lopez@licican.local', 'administrador de plataforma', 'activo', 'Cuenta administrativa principal.', '2026-04-01T09:00:00Z', '2026-04-02T08:10:00Z', FALSE),
    ('usr-002', 'Carlos', 'Mendez', 'carlos.mendez@licican.local', 'administrador funcional', 'activo', 'Apoyo funcional de operaciones.', '2026-04-01T10:15:00Z', '2026-04-02T07:50:00Z', FALSE),
    ('usr-003', 'Laura', 'Gonzalez', 'laura.gonzalez@licican.local', 'responsable', 'pendiente', 'Invitacion pendiente de activacion.', '2026-04-02T08:30:00Z', NULL, TRUE),
    ('usr-004', 'Mario', 'Perez', 'mario.perez@licican.local', 'colaborador', 'inactivo', 'Usuario en pausa operativa.', '2026-03-30T11:00:00Z', '2026-03-31T15:15:00Z', FALSE)
ON CONFLICT (id) DO NOTHING;

INSERT INTO usuario_historial (usuario_id, accion, fecha, detalle)
VALUES
    ('usr-001', 'alta', '2026-04-01T09:00:00Z', 'Alta inicial de la cuenta administrativa.'),
    ('usr-001', 'acceso', '2026-04-02T08:10:00Z', 'Acceso de verificacion en el entorno de producto.'),
    ('usr-002', 'alta', '2026-04-01T10:15:00Z', 'Alta de administracion funcional.'),
    ('usr-003', 'alta', '2026-04-02T08:30:00Z', 'Invitacion inicial enviada.'),
    ('usr-004', 'alta', '2026-03-30T11:00:00Z', 'Alta inicial de colaborador.'),
    ('usr-004', 'desactivacion', '2026-04-01T12:00:00Z', 'Cuenta desactivada temporalmente.')
ON CONFLICT (usuario_id, fecha, accion, detalle) DO NOTHING;

COMMENT ON TABLE usuario IS 'Cuentas administrativas de la aplicación Licican';
COMMENT ON COLUMN usuario.id IS 'Identificador funcional estable de la cuenta';
COMMENT ON COLUMN usuario.nombre IS 'Nombre de pila del usuario';
COMMENT ON COLUMN usuario.apellidos IS 'Apellidos del usuario';
COMMENT ON COLUMN usuario.email IS 'Correo electrónico único de la cuenta';
COMMENT ON COLUMN usuario.rol_principal IS 'Rol funcional principal asignado';
COMMENT ON COLUMN usuario.estado IS 'Estado operativo de la cuenta: activo, inactivo, pendiente, bloqueado o baja logica';
COMMENT ON COLUMN usuario.observaciones_internas IS 'Notas internas no visibles para el acceso de usuario final';
COMMENT ON COLUMN usuario.fecha_alta IS 'Fecha de alta administrativa de la cuenta';
COMMENT ON COLUMN usuario.ultimo_acceso IS 'Último acceso registrado por la plataforma';
COMMENT ON COLUMN usuario.invitacion_pendiente IS 'Indica si la cuenta aún debe activar la invitación';

COMMENT ON TABLE usuario_historial IS 'Trazabilidad histórica de cambios sobre cuentas de usuario';
COMMENT ON COLUMN usuario_historial.usuario_id IS 'Identificador de la cuenta afectada por el evento';
COMMENT ON COLUMN usuario_historial.accion IS 'Tipo de evento registrado sobre la cuenta';
COMMENT ON COLUMN usuario_historial.fecha IS 'Momento UTC del evento';
COMMENT ON COLUMN usuario_historial.detalle IS 'Descripción operativa del cambio o acceso';
-- ============================================================
-- Comentarios descriptivos
-- ============================================================
COMMENT ON TABLE  licitacion IS 'Licitaciones del Sector Público de España (fuente: contrataciondelestado.es)';
COMMENT ON COLUMN licitacion.id_plataforma IS 'Identificador único de la licitación en la plataforma (URL de sindicación Atom)';
COMMENT ON COLUMN licitacion.expediente IS 'Número de expediente del órgano de contratación';
COMMENT ON COLUMN licitacion.estado IS 'Código de estado: EV=Evaluación, ADJ=Adjudicada, RES=Resuelta, PUB=Publicada, etc.';
COMMENT ON COLUMN licitacion.updated_at IS 'Fecha de última actualización del registro en la fuente Atom';
COMMENT ON COLUMN licitacion.entry_xml IS 'XML completo del entry Atom para reprocesamiento futuro';
