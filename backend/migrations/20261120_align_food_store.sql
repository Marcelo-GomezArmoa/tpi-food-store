BEGIN;

DO $$
BEGIN
    IF current_database() <> 'food_store' THEN
        RAISE EXCEPTION 'Esta migracion debe ejecutarse en food_store';
    END IF;
END
$$;

LOCK TABLE categoria, producto, pedido IN ACCESS EXCLUSIVE MODE;

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pedido) THEN
        RAISE EXCEPTION 'Hay pedidos existentes: se requiere definir sus propietarios antes de migrar';
    END IF;
END
$$;

ALTER TABLE categoria ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE producto ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE pedido ADD COLUMN usuario_id INTEGER NOT NULL REFERENCES usuario (id);

CREATE INDEX ix_categoria_deleted_at ON categoria (deleted_at);
CREATE INDEX ix_producto_deleted_at ON producto (deleted_at);
CREATE INDEX ix_pedido_usuario_id ON pedido (usuario_id);

COMMIT;
