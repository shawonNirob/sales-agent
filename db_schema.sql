-- Table: webshop.address

-- DROP TABLE IF EXISTS webshop.address;

CREATE TABLE IF NOT EXISTS webshop.address
(
    id integer NOT NULL DEFAULT nextval('webshop.address_id_seq'::regclass),
    customerid integer,
    firstname text COLLATE pg_catalog."default",
    lastname text COLLATE pg_catalog."default",
    address1 text COLLATE pg_catalog."default",
    address2 text COLLATE pg_catalog."default",
    city text COLLATE pg_catalog."default",
    zip text COLLATE pg_catalog."default",
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT address_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.address
    OWNER to postgres;

COMMENT ON TABLE webshop.address
    IS 'Addresses for receipts and shipping';

--------------------------------------------------------------------------------
-- Table: webshop.articles

-- DROP TABLE IF EXISTS webshop.articles;

CREATE TABLE IF NOT EXISTS webshop.articles
(
    id integer NOT NULL DEFAULT nextval('webshop.articles_id_seq'::regclass),
    productid integer,
    ean text COLLATE pg_catalog."default",
    colorid integer,
    size integer,
    description text COLLATE pg_catalog."default",
    originalprice money,
    reducedprice money,
    taxrate numeric,
    discountinpercent integer,
    currentlyactive boolean,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT articles_pkey PRIMARY KEY (id),
    CONSTRAINT articles_colorid_fkey FOREIGN KEY (colorid)
        REFERENCES webshop.colors (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.articles
    OWNER to postgres;

COMMENT ON TABLE webshop.articles
    IS 'Instance of a product with a size, color and price';
--------------------------------------------------------------------------------

-- Table: webshop.colors

-- DROP TABLE IF EXISTS webshop.colors;

CREATE TABLE IF NOT EXISTS webshop.colors
(
    id integer NOT NULL DEFAULT nextval('webshop.colors_id_seq'::regclass),
    name text COLLATE pg_catalog."default",
    rgb text COLLATE pg_catalog."default",
    CONSTRAINT colors_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.colors
    OWNER to postgres;

COMMENT ON TABLE webshop.colors
    IS 'Colors with name and rgb value';

--------------------------------------------------------------------------------

-- Table: webshop.customer

-- DROP TABLE IF EXISTS webshop.customer;

CREATE TABLE IF NOT EXISTS webshop.customer
(
    id integer NOT NULL DEFAULT nextval('webshop.customer_id_seq1'::regclass),
    firstname text COLLATE pg_catalog."default",
    lastname text COLLATE pg_catalog."default",
    gender gender,
    email text COLLATE pg_catalog."default",
    dateofbirth date,
    currentaddressid integer,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT customer_pkey1 PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.customer
    OWNER to postgres;

COMMENT ON TABLE webshop.customer
    IS 'Basic customer data';

--------------------------------------------------------------------------------

-- Table: webshop.labels

-- DROP TABLE IF EXISTS webshop.labels;

CREATE TABLE IF NOT EXISTS webshop.labels
(
    id integer NOT NULL DEFAULT nextval('webshop.labels_id_seq'::regclass),
    name text COLLATE pg_catalog."default",
    slugname text COLLATE pg_catalog."default",
    icon bytea,
    CONSTRAINT labels_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.labels
    OWNER to postgres;

COMMENT ON TABLE webshop.labels
    IS 'Brands / labels';
--------------------------------------------------------------------------------
-- Table: webshop.order

-- DROP TABLE IF EXISTS webshop."order";

CREATE TABLE IF NOT EXISTS webshop."order"
(
    id integer NOT NULL DEFAULT nextval('webshop.order_id_seq'::regclass),
    customer integer,
    ordertimestamp timestamp with time zone DEFAULT now(),
    shippingaddressid integer,
    total money,
    shippingcost money,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT order_pkey PRIMARY KEY (id),
    CONSTRAINT order_shippingaddressid_fkey FOREIGN KEY (shippingaddressid)
        REFERENCES webshop.address (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop."order"
    OWNER to postgres;

COMMENT ON TABLE webshop."order"
    IS 'Metadata for an order, see order_positions as well';
--------------------------------------------------------------------------------

-- Table: webshop.order_positions

-- DROP TABLE IF EXISTS webshop.order_positions;

CREATE TABLE IF NOT EXISTS webshop.order_positions
(
    id integer NOT NULL DEFAULT nextval('webshop.order_positions_id_seq'::regclass),
    orderid integer,
    articleid integer,
    amount smallint,
    price money,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT order_positions_pkey PRIMARY KEY (id),
    CONSTRAINT order_positions_articleid_fkey FOREIGN KEY (articleid)
        REFERENCES webshop.articles (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT order_positions_orderid_fkey FOREIGN KEY (orderid)
        REFERENCES webshop."order" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.order_positions
    OWNER to postgres;

COMMENT ON TABLE webshop.order_positions
    IS 'Articles that are contained in an order';
--------------------------------------------------------------------------------

-- Table: webshop.products

-- DROP TABLE IF EXISTS webshop.products;

CREATE TABLE IF NOT EXISTS webshop.products
(
    id integer NOT NULL DEFAULT nextval('webshop.products_id_seq'::regclass),
    name text COLLATE pg_catalog."default",
    labelid integer,
    category category,
    gender gender,
    currentlyactive boolean,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT products_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.products
    OWNER to postgres;

COMMENT ON TABLE webshop.products
    IS 'Groups articles (differing in sizes/color)';
--------------------------------------------------------------------------------
-- Table: webshop.sizes

-- DROP TABLE IF EXISTS webshop.sizes;

CREATE TABLE IF NOT EXISTS webshop.sizes
(
    id integer NOT NULL DEFAULT nextval('webshop.sizes_id_seq'::regclass),
    gender gender,
    category category,
    size text COLLATE pg_catalog."default",
    size_us int4range,
    size_uk int4range,
    size_eu int4range,
    CONSTRAINT sizes_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.sizes
    OWNER to postgres;

COMMENT ON TABLE webshop.sizes
    IS 'Colors with name and rgb value';

--------------------------------------------------------------------------------
-- Table: webshop.stock

-- DROP TABLE IF EXISTS webshop.stock;

CREATE TABLE IF NOT EXISTS webshop.stock
(
    id integer NOT NULL DEFAULT nextval('webshop.stock_id_seq'::regclass),
    articleid integer,
    count integer,
    created timestamp with time zone DEFAULT now(),
    updated timestamp with time zone,
    CONSTRAINT stock_pkey PRIMARY KEY (id),
    CONSTRAINT stock_articleid_fkey FOREIGN KEY (articleid)
        REFERENCES webshop.articles (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS webshop.stock
    OWNER to postgres;

COMMENT ON TABLE webshop.stock
    IS 'Amount of articles on stock';

--------------------------------------------------------------------------------
