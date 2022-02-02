-- Example Postgres schema matching the dataset in public/data/dataset/postgres_example_dataset.yml
DROP TABLE IF EXISTS public.report;
DROP TABLE IF EXISTS public.service_request;
DROP TABLE IF EXISTS public.login;
DROP TABLE IF EXISTS public.visit;
DROP TABLE IF EXISTS public.order_item;
DROP TABLE IF EXISTS public.orders;
DROP TABLE IF EXISTS public.payment_card;
DROP TABLE IF EXISTS public.employee;
DROP TABLE IF EXISTS public.customer;
DROP TABLE IF EXISTS public.address;
DROP TABLE IF EXISTS public.product;
DROP TABLE IF EXISTS public.composite_pk_test;
DROP TABLE IF EXISTS public.type_link_test;


CREATE TABLE public.product (
    id INT PRIMARY KEY,
    name CHARACTER VARYING(100),
    price MONEY
);

CREATE TABLE public.address (
    id BIGINT PRIMARY KEY,
    house INT,
    street CHARACTER VARYING(100),
    city CHARACTER VARYING(100),
    state CHARACTER VARYING(100),
    zip CHARACTER VARYING(100)
);

CREATE TABLE public.customer (
    id INT PRIMARY KEY,
    email CHARACTER VARYING(100),
    name  CHARACTER VARYING(100),
    created TIMESTAMP,
    address_id BIGINT
);

CREATE TABLE public.employee (
    id INT PRIMARY KEY,
    email CHARACTER VARYING(100),
    name CHARACTER VARYING(100),
    address_id BIGINT
);

CREATE TABLE public.payment_card (
    id CHARACTER VARYING(100) PRIMARY KEY,
    name CHARACTER VARYING(100),
    ccn BIGINT,
    code SMALLINT,
    preferred BOOLEAN,
    customer_id INT,
    billing_address_id BIGINT
);

CREATE TABLE public.orders (
    id CHARACTER VARYING(100) PRIMARY KEY,
    customer_id INT,
    shipping_address_id BIGINT,
    payment_card_id CHARACTER VARYING(100)
);

CREATE TABLE public.order_item (
    order_id CHARACTER VARYING(100),
    item_no SMALLINT,
    product_id INT,
    quantity SMALLINT,
    CONSTRAINT order_item_pk PRIMARY KEY (order_id, item_no)
);

CREATE TABLE public.visit (
    email CHARACTER VARYING(100),
    last_visit TIMESTAMP,
    CONSTRAINT visit_pk PRIMARY KEY (email, last_visit)
);

CREATE TABLE public.login (
    id INT PRIMARY KEY,
    customer_id INT,
    time TIMESTAMP
);

CREATE TABLE public.service_request (
    id CHARACTER VARYING(100) PRIMARY KEY,
    email CHARACTER VARYING(100),
    alt_email CHARACTER VARYING(100),
    opened DATE,
    closed DATE,
    employee_id INT
);

CREATE TABLE public.report (
    id INT PRIMARY KEY,
    email CHARACTER VARYING(100),
    name CHARACTER VARYING(100),
    year INT,
    month INT,
    total_visits INT
);

CREATE TABLE public.composite_pk_test (
    id_a INT NOT NULL,
    id_b INT NOT NULL,
    description VARCHAR(100),
    customer_id INT,
    PRIMARY KEY(id_a, id_b)
);

CREATE TABLE public.type_link_test (
    id CHARACTER VARYING(100) PRIMARY KEY,
    name CHARACTER VARYING(100)
);
