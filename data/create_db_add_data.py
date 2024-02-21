# Create database and import data from CSV to database table using sqlite3
from pathlib import Path
import sqlite3
import pandas as pd


def create_db():
    """Create SQLite database with data.

    Create the database outside the Flask application code.
    """

    # 1. Create a SQLite database engine that connects to the database file
    db_file = Path(__file__).parent.parent.joinpath("database.sqlite")
    connection = sqlite3.connect(db_file)

    # 2. Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # 2. Define the tables in SQL
    # 'course' table definition in SQL
    create_course_table = """CREATE TABLE if not exists course(
                    COURSE_INDEX INTEGER PRIMARY KEY,
                    COURSE TEXT NOT NULL,
                    KISMODE INTEGER NOT NULL);
                    """

    # 'employment' table definition in SQL
    create_employment_table = """CREATE TABLE if not exists employment(
        COURSE_INDEX INTEGER,
        EMP_ROW_ID INTEGER PRIMARY KEY,
        STUDY INTEGER,
        UNEMP INTEGER,
        PREVWORKSTUD INTEGER,
        BOTH INTEGER,
        NOAVAIL INTEGER,
        WORK INTEGER,
        FOREIGN KEY(COURSE_INDEX) REFERENCES course(COURSE_INDEX));"""
    
    # 'satisfaction' table definition in SQL
    create_satisfaction_table = """CREATE TABLE if not exists satisfaction(
        COURSE_INDEX INTEGER,
        SAT_ROW_ID INTEGER PRIMARY KEY,
        GOWORKMEAN INTEGER,
        GOWORKONTRACK INTEGER,
        GOWORKSKILLS INTEGER,
        FOREIGN KEY(COURSE_INDEX) REFERENCES course(COURSE_INDEX));"""

    # 'salary' table definition in SQL
    create_salary_table = """CREATE TABLE if not exists salary(
        COURSE_INDEX INTEGER,
        SAL_ROW_ID INTEGER PRIMARY KEY,
        KISLEVEL INTEGER NOT NULL,
        GOSECLQ_UK INTEGER NOT NULL,
        GOSECMED_UK INTEGER NOT NULL,
        GOSECUQ_UK INTEGER NOT NULL,
        GOSECLQ_E INTEGER NOT NULL,
        GOSECMED_E INTEGER NOT NULL,
        GOSECUQ_E INTEGER NOT NULL,
        GOSECLQ_NI INTEGER NOT NULL,
        GOSECMED_NI INTEGER NOT NULL,
        GOSECUQ_NI INTEGER NOT NULL,
        GOSECLQ_S INTEGER NOT NULL,
        GOSECMED_S INTEGER NOT NULL,
        GOSECUQ_S INTEGER NOT NULL,
        GOSECLQ_W INTEGER NOT NULL,
        GOSECMED_W INTEGER NOT NULL,
        GOSECUQ_W INTEGER NOT NULL,
        FOREIGN KEY(COURSE_INDEX) REFERENCES course(COURSE_INDEX));"""

    # 4. Execute SQL to create the tables in the database
    cursor.execute(create_course_table)
    cursor.execute(create_employment_table)
    cursor.execute(create_satisfaction_table)
    cursor.execute(create_salary_table)

    # 5. Commit the changes to the database (this saves the tables created in the previous step)
    connection.commit()

    # 6. Import data from CSV to database table using pandas
    # Read the course data to a pandas dataframe
    na_values = ["", ]
    course_file = Path(__file__).parent.joinpath("COURSE.csv")
    course_df = pd.read_csv(course_file, keep_default_na=False, na_values=na_values)

    # Read the employment data to a pandas dataframe
    employment_file = Path(__file__).parent.joinpath("EMPLOYMENT.csv")
    employment_df = pd.read_csv(employment_file)

     # Read the satsfaction data to a pandas dataframe
    satisfaction_file = Path(__file__).parent.joinpath("SATISFACTION.csv")
    satisfaction_df = pd.read_csv(satisfaction_file)

    # Read the salary data to a pandas dataframe
    salary_file = Path(__file__).parent.joinpath("SALARY.csv")
    salary_df = pd.read_csv(salary_file)

    # 7. Write the pandas DataFrame contents to the database tables
    # For all the tables we do not want the pandas DataFrame index column
    course_df.to_sql("course", connection, if_exists="append", index=False)
    employment_df.to_sql("employment", connection, if_exists="append", index=False)
    satisfaction_df.to_sql("satisfaction", connection, if_exists="append", index=False)
    salary_df.to_sql("salary", connection, if_exists="append", index=False)

    # 8. Close the database connection
    connection.close()


if __name__ == '__main__':
    create_db()
