# Additional Database Tables Created    

def create_employee_info_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AIAI_Employee_Info')
        BEGIN 
            CREATE TABLE AIAI_Employee_Info (
                production_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                user_key VARCHAR(255) UNIQUE,
                First_Name VARCHAR(255),
                Middle_Name VARCHAR(255),
                Last_Name VARCHAR(255),
                ID VARCHAR(255) UNIQUE,
                Email VARCHAR(255),
                Employee_Password VARCHAR(255),
                Address VARCHAR(255),
                Apt_Number VARCHAR(255),
                City VARCHAR(255),
                State VARCHAR(255),
                Zip_Code VARCHAR(255),
                Phone_Number VARCHAR(255),
                Employee_Username VARCHAR(255),
                Title VARCHAR(255),
                is_admin INT,
                is_installer INT,
                failed_attempts INT,
                time_hashed BIGINT,
                license_key VARCHAR(255),
                verification_key VARCHAR(255),
                stripe_charge_id VARCHAR(255),
                pin VARCHAR(255),
                hire_date DATE,
                is_active INT NOT NULL DEFAULT 0,
                subscription_plan NVARCHAR(50),
                created_at DATETIME2                
            )
        END
    ''')

def create_builders_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AIAI_Builders_Info')
        BEGIN
            CREATE TABLE AIAI_Builders_Info (
                builder_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                builder_name VARCHAR(255),
                jobsite_name VARCHAR(255),
                jobsite_address VARCHAR(255),
                city VARCHAR(255),
                state VARCHAR(255),
                zip_code VARCHAR(255),
                model_name VARCHAR(255),
                jobsite_lot_number VARCHAR(255),
                builder_block_number VARCHAR(255),
                job_total_sq_ft VARCHAR(255),
                ext_block_sq_footage VARCHAR(255),
                ceiling_area_sq_footage VARCHAR(255),
                garage_ceiling_sq_footage VARCHAR(255),
                garage_wall_sq_footage VARCHAR(255),
                int_wall_sq_footage VARCHAR(255),
                miscellaneous_info VARCHAR(MAX)
            )
        END
    ''')

def create_weekly_payroll_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AIAI_Weekly_Payroll')
        BEGIN
            CREATE TABLE AIAI_Weekly_Payroll (
                payroll_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                Time TIME NOT NULL,
                MM_DD_YYYY DATETIME2 NOT NULL,
                Day_of_Week DATETIME2 NOT NULL,
                First_Name VARCHAR(255) NOT NULL,
                Last_Name VARCHAR(255) NOT NULL,
                Employee_ID INT,
                Salt VARCHAR(255) NOT NULL,
                Employee_Hours INT NOT NULL,
                Employee_Job_Title VARCHAR(255),
                Builder VARCHAR(255),
                Jobsite VARCHAR(255),
                Model_Name VARCHAR(255),
                Lot_Number INT,
                Block_Number INT,
                Material_Used DECIMAL(18,2),
                Material_Used_2 DECIMAL(18,2),
                Material_Used_3 DECIMAL(18,2),
                Material_Used_4 DECIMAL(18,2),
                Material_Used_5 DECIMAL(18,2),
                Material_Used_6 DECIMAL(18,2),
                Material_Used_7 DECIMAL(18,2),
                R_Value DECIMAL(18,2),
                R_Value_2 DECIMAL(18,2),
                R_Value_3 DECIMAL(18,2),
                R_Value_4 DECIMAL(18,2),
                R_Value_5 DECIMAL(18,2),
                R_Value_6 DECIMAL(18,2),
                R_Value_7 DECIMAL(18,2),
                Material_Width DECIMAL(18,2),
                Material_Width_2 DECIMAL(18,2),
                Material_Width_3 DECIMAL(18,2),
                Material_Width_4 DECIMAL(18,2),
                Material_Width_5 DECIMAL(18,2),
                Material_Width_6 DECIMAL(18,2),
                Material_Width_7 DECIMAL(18,2),
                Sqft_Bags_Installed DECIMAL(18,2),
                Sqft_Bags_Installed_2 DECIMAL(18,2),
                Sqft_Bags_Installed_3 DECIMAL(18,2),
                Sqft_Bags_Installed_4 DECIMAL(18,2),
                Sqft_Bags_Installed_5 DECIMAL(18,2),
                Sqft_Bags_Installed_6 DECIMAL(18,2),
                Sqft_Bags_Installed_7 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_2 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_3 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_4 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_5 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_6 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_7 DECIMAL(18,2),
                Pay DECIMAL(18,2),
                Pay_2 DECIMAL(18,2),
                Pay_3 DECIMAL(18,2),
                Pay_4 DECIMAL(18,2),
                Pay_5 DECIMAL(18,2),
                Pay_6 DECIMAL(18,2),
                Pay_7 DECIMAL(18,2),
                total_pay DECIMAL(18,2),
                Pay_Per_Employee DECIMAL(18,2),
                Split_Pay_Per_Employee DECIMAL(18,2)
            )
        END
    ''')

def create_material_info_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AIAI_Material_Info')
        BEGIN
            CREATE TABLE AIAI_Material_Info (
                material_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                material_code VARCHAR(255),
                material_name VARCHAR(255),
                material_r_value VARCHAR(255),
                material_width INT,
                square_footage INT,
                pay_rate DECIMAL(18,2)
            )
        END
    ''')

def create_employee_weekly_payroll_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'AIAI_Employee_Weekly_Payroll')
        BEGIN
            CREATE TABLE AIAI_Employee_Weekly_Payroll (
                employee_payroll_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                Time TIME NOT NULL,
                MM_DD_YYYY DATETIME2 NOT NULL,
                Day_of_Week DATETIME2 NOT NULL,
                First_Name VARCHAR(255) NOT NULL,
                Last_Name VARCHAR(255) NOT NULL,
                Employee_ID INT,
                Salt VARCHAR(255) NOT NULL,
                Employee_Hours INT NOT NULL,
                Employee_Job_Title VARCHAR(255),
                Builder VARCHAR(255),
                Jobsite VARCHAR(255),
                Model_Name VARCHAR(255),
                Lot_Number INT,
                Block_Number INT,
                Material_Used INT,
                Material_Used_2 INT,
                Material_Used_3 INT,
                Material_Used_4 INT,
                Material_Used_5 INT,
                Material_Used_6 INT,
                Material_Used_7 INT,
                R_Value INT,
                R_Value_2 INT,
                R_Value_3 INT,
                R_Value_4 INT,
                R_Value_5 INT,
                R_Value_6 INT,
                R_Value_7 INT,
                Material_Width INT,
                Material_Width_2 INT,
                Material_Width_3 INT,
                Material_Width_4 INT,
                Material_Width_5 INT,
                Material_Width_6 INT,
                Material_Width_7 INT,
                Sqft_Bags_Installed INT,
                Sqft_Bags_Installed_2 INT,
                Sqft_Bags_Installed_3 INT,
                Sqft_Bags_Installed_4 INT,
                Sqft_Bags_Installed_5 INT,
                Sqft_Bags_Installed_6 INT,
                Sqft_Bags_Installed_7 INT,
                Pay_Per_Tube_Piece_Rate DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_2 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_3 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_4 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_5 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_6 DECIMAL(18,2),
                Pay_Per_Tube_Piece_Rate_7 DECIMAL(18,2),
                Pay DECIMAL(18,2),
                Pay_2 DECIMAL(18,2),
                Pay_3 DECIMAL(18,2),
                Pay_4 DECIMAL(18,2),
                Pay_5 DECIMAL(18,2),
                Pay_6 DECIMAL(18,2),
                Pay_7 DECIMAL(18,2),
                total_pay DECIMAL(18,2),
                Pay_Per_Employee DECIMAL(18,2),
                Split_Pay_Per_Employee DECIMAL(18,2)
            )
        END
    ''')

def create_pay_week_schedule_table(cursor):
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'pay_week')
        BEGIN
            CREATE TABLE pay_week (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                start_day DATETIME2,
                end_day DATETIME2
            )
        END
    ''')

def initialize_all_tables(cursor, conn):
    create_employee_info_table(cursor)
    create_builders_table(cursor)
    create_weekly_payroll_table(cursor)
    create_material_info_table(cursor)
    create_employee_weekly_payroll_table(cursor)
    create_pay_week_schedule_table(cursor)
    conn.commit()