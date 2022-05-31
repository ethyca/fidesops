import sqlalchemy

MASTER_MSSQL_URL = ""


SUPPORTED_DATA_TYPES = set(
    [
        # char types
        "varchar",
        "nvarchar",
        "char",
        "nchar",
        "ntext",
        "text",
        # numeric types
        "int",
        "bigint",
        "smallint",
        "tinyint",
        "money",
        "float",
        "decimal",
        # date types
        "date",
        "datetime",
        "datetime2",
        "smalldatetime",
        # other types
        "bit",
    ]
)


def mssql_discover():
    """
    Select all databases from the instance
    Select the schema data for each data base
    Check if there are any fields in the schema that Fidesops does not yet support
    """
    engine = sqlalchemy.create_engine(MASTER_MSSQL_URL)
    all_dbs = engine.execute("SELECT name FROM sys.databases;").all()
    all_columns = []
    flagged_columns = []
    flagged_datatypes = set()
    for db_name in all_dbs:
        db_name = db_name[0]
        try:
            columns = engine.execute(
                f"SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM {db_name}.INFORMATION_SCHEMA.COLUMNS;"
            ).all()
        except Exception:
            # print(f"Access to {db_name}'s tables denied.")
            continue

        all_columns.extend(columns)
        for table, column, data_type, nullable in columns:
            if data_type not in SUPPORTED_DATA_TYPES:
                flagged_datatypes.add(data_type)
                flagged_columns.append(f"{table}.{column}: {data_type}")

    print(f"{len(set(all_columns))} columns found")
    print(f"{len(set(flagged_columns))} columns flagged")
    print(f"Flagged datatypes:")
    print(",\n".join(flagged_datatypes))
    print(f"Flagged columns:")
    print(",\n".join(flagged_columns))


if __name__ == "__main__":
    mssql_discover()
