-- Example Postgres schema matching the dataset in public/data/dataset/comprehensive_test_dataset.yml
DROP TABLE IF EXISTS public.postgres_types;


CREATE TABLE public.postgres_types (
    id INT PRIMARY KEY NULL,
    email VARCHAR UNIQUE NULL,
    int_column INT NULL,
    float_column FLOAT NULL,
    -- serial_column SERIAL,  # SERIAL columns are not nullable
    money_column MONEY NULL,
    char_column CHAR NULL,
    varchar_column VARCHAR NULL,
    text_column TEXT NULL
);


INSERT INTO public.postgres_types VALUES
(
    1,
    '1@example.com',
    111,
    1.11,
    -- DEFAULT,
    '$10.00',
    'a',
    'abc',
    'a big chunk of text'
);
