import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from mlproject.logger import logging
from mlproject.exception import CustomException
import pandas as pd
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine

load_dotenv()

host= os.getenv('host')
user= os.getenv('user')
password= os.getenv('password')
db= os.getenv('db')

def read_sql_data():
    logging.info('Reading SQL database started')
    try:
        # Establishing connection to the MySQL database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Sidra123@',
            db='college'
        )
        print("Connection successful")

        # Creating an engine for SQLAlchemy
        engine = create_engine("mysql+pymysql://root:Sidra123@127.0.0.1:3306/college")

        # Reading data into a DataFrame
        df = pd.read_sql_query('SELECT * FROM `college.students`;', connection)

        print(df.head())
        return df

    except pymysql.err.OperationalError as e:
        print(f"Error: {e}")

    # finally:
    #     # Closing the connection
    #     if 'connection' in locals():
    #         connection.close()




# def read_sql_data():
#     logging.info('Reading SQL database started')
#     try:
#         connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='Sidra123@',  # Use the same password you used in MySQL CLI
#         db='college'
#     )
#     print("Connection successful")
#     engine = create_engine("mysql+pymysql://root:Sidra123@127.0.0.1:3306/college")

#     df =pd.read_sql_query('SELECT * FROM college.`college.students`;', connection)

#     print(df.head())

#     return df

#     except pymysql.err.OperationalError as e:
#     print(f"Error: {e}")
    
 
