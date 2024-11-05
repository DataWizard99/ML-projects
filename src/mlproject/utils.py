import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from mlproject.logger import logging
from mlproject.exception import CustomException
import pandas as pd
from dotenv import load_dotenv
import pymysql
# from sqlalchemy import create_engine
import pickle
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


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
        # engine = create_engine("mysql+pymysql://root:Sidra123@127.0.0.1:3306/college")

        # Reading data into a DataFrame
        df = pd.read_sql_query('SELECT * FROM `college.students`;', connection)

        print(df.head())
        return df

    except pymysql.err.OperationalError as e:
        print(f"Error: {e}")

def save_object(file_path, obj):
    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    
    

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report= {}
        for i in range(len(list(models))):
            model = list(models.values())[i]  # Convert dict values to a list

            para = param[list(models.keys())[i]]  # Convert dict keys to a list


            gs= GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred= model.predict(X_train)
            y_test_pred= model.predict(X_test)
            
            train_model_score= r2_score(y_train, y_train_pred)
            test_model_score= r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]]= test_model_score

        return report
    
        
    
    except Exception as e:
        raise CustomException(e, sys)

   





 
