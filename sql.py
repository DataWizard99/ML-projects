import pymysql
import pandas as pd
from sqlalchemy import create_engine
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Sidra123@',  # Use the same password you used in MySQL CLI
        db='college'
    )
    print("Connection successful")
    engine = create_engine("mysql+pymysql://root:Sidra123@127.0.0.1:3306/college")

    df =pd.read_sql_query('SELECT * FROM college.`college.students`;', connection)


    print(df.head())

    
except pymysql.err.OperationalError as e:
    print(f"Error: {e}")
