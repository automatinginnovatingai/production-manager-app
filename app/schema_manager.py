def ensure_schema(cursor, conn):
    # 1. Check if schema_version table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM sys.tables 
        WHERE name = 'schema_version'
    """)
    exists = cursor.fetchone()[0]

    if exists == 0:
        # 2. Create schema_version table
        cursor.execute("""
            CREATE TABLE schema_version (
                version INT NOT NULL
            );
        """)

        # 3. Run your existing table creation modules
        from create_db_table import initialize_database
        from create_additional_db_table import initialize_all_tables

        # These functions already contain IF NOT EXISTS checks
        initialize_database(cursor, conn)
        initialize_all_tables(cursor, conn)

        # 4. Insert version row
        cursor.execute("INSERT INTO schema_version (version) VALUES (1);")

        conn.commit()