# ---------- Table Creation Functions ----------

def create_subscription_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'subscription')
        BEGIN
            CREATE TABLE subscription (
                customer_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                subscription_id VARCHAR(255),
                customer_name VARCHAR(255),
                payment DECIMAL(19,4),
                status VARCHAR(255),
                subscription_plan VARCHAR(255),
                salt VARCHAR(255),
                plan_id VARCHAR(255),
                start_date DATETIME2,
                end_date DATETIME2,
                subscription_start_date DATETIME2,
                next_billing_date DATETIME2,
                subscription_end_date DATETIME2,
                payment_status VARCHAR(255),
                monthly_fee VARCHAR(255),
                employee_count VARCHAR(255),
                company_id UNIQUEIDENTIFIER NOT NULL,
                FOREIGN KEY (company_id) REFERENCES companies(company_id),
                FOREIGN KEY (customer_id) REFERENCES subscription(customer_id)
            )
        END
    ''')

def add_user_data(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
        BEGIN
            CREATE TABLE users (
                user_key UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                first_name VARCHAR(255),
                middle_name VARCHAR(255),      
                last_name VARCHAR(255),
                phone_number VARCHAR(255) UNIQUE,
                email VARCHAR(255) UNIQUE,
                pin VARCHAR(255),   
                license_key VARCHAR(255) UNIQUE,
                verification_key VARCHAR(255) UNIQUE,
                agreed VARCHAR(255),
                salt VARCHAR(255),
                hire_date DATE,
                is_admin VARCHAR(255),
                employee_id VARCHAR(255),   
                failed_attempts INT,
                time_hashed BIGINT,
                company_id UNIQUEIDENTIFIER NOT NULL,                  
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            )
        END
    ''')

def create_companies_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'companies')
        BEGIN
            CREATE TABLE companies (
                company_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                company_user_key VARCHAR(255) UNIQUE,
                company_name VARCHAR(255),
                company_address VARCHAR(255),
                city VARCHAR(255),
                state VARCHAR(255),
                zip_code VARCHAR(255),
                company_phone_number VARCHAR(255),
                company_email VARCHAR(255) UNIQUE,
                company_tax_id VARCHAR(255),
                contractor_license VARCHAR(255),
                company_pin VARCHAR(MAX),
                registration_status TEXT DEFAULT 'pending',
                license_key VARCHAR(255) UNIQUE,
                verification_key VARCHAR(255) UNIQUE,
                salt VARCHAR(255),
                customer_id VARCHAR(255),
                subscription_plan VARCHAR(255),
                monthly_fee DECIMAL(18, 2),
                additional_user_fee DECIMAL(18, 2),
                subscription_id VARCHAR(255),
                status VARCHAR(255),
                agreed VARCHAR(255),
                payment_status VARCHAR(255),
                UNIQUE(company_name, company_tax_id)   
            )
        END
    ''')

def create_activations_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'activations')
        BEGIN
            CREATE TABLE activations (
                activation_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                gumroad_key_hash VARBINARY(64) NOT NULL,
                installer_id INT NOT NULL,
                plan NVARCHAR(50) NOT NULL,
                created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
            );
        END
    """)

def create_admin_activations_table(cursor):
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'admin_licenses'
        )
        BEGIN
            CREATE TABLE admin_licenses (
                admin_id UNIQUEIDENTIFIER NOT NULL,
                license_hash VARBINARY(64) NOT NULL,
                plan_type NVARCHAR(50) NOT NULL,
                activated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                is_main_admin BIT NOT NULL DEFAULT 0,
                CONSTRAINT PK_admin_licenses PRIMARY KEY (admin_id),
                CONSTRAINT FK_admin_licenses_users FOREIGN KEY (admin_id)
                REFERENCES users(user_key)
            );
        END
    """)
def initialize_database(cursor, conn):
    create_companies_table(cursor)
    add_user_data(cursor)
    create_subscription_table(cursor)
    create_activations_table(cursor)
    create_admin_activations_table(cursor)
    conn.commit()
