def ensure_schema(cursor, conn):
    # Check if schema_version table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM sys.tables
        WHERE name = 'schema_version'
    """)
    exists = cursor.fetchone()[0]

    if exists == 0:
        # Create schema_version table
        cursor.execute("""
            CREATE TABLE schema_version (
                version INT NOT NULL
            );
        """)

        # Import schema creation modules
        from create_db_table import initialize_database
        from create_additional_db_table import initialize_all_tables

        # Run full schema initialization (tables + procedures)
        initialize_database(cursor, conn)
        initialize_all_tables(cursor, conn)

        # Insert version row
        cursor.execute("INSERT INTO schema_version (version) VALUES (1);")
        conn.commit()

    else:
        # Schema exists — refresh stored procedures only
        from create_additional_db_table import initialize_all_tables
        initialize_all_tables(cursor, conn)
        conn.commit()