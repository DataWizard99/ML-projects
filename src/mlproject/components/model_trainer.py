import sys
import os
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
import mlflow
from urllib.parse import urlparse
import mlflow.sklearn
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from mlproject.logger import logging
from mlproject.exception import CustomException
from mlproject.utils import save_object, evaluate_models
@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts", "model.pickl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()


    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def Initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("split training and test input data")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            Models = {
           "Linear Regression": LinearRegression(),
           "Lasso": Lasso(),
           "Ridge": Ridge(),
           "K-Neighbors Regressor": KNeighborsRegressor(),
           "Decision Tree": DecisionTreeRegressor(),
           "Random Forest Regressor": RandomForestRegressor(),
           "XGBRegressor": XGBRegressor(), 
           "CatBoosting Regressor": CatBoostRegressor(verbose=False),
           "AdaBoost Regressor": AdaBoostRegressor()
              }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest Regressor":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "Lasso": {},  # Add this line for Lasso
                "Ridge": {},
                "K-Neighbors Regressor": {},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            print("X_train shape:", X_train.shape)
            print("y_train shape:", y_train.shape)
            print("X_test shape:", X_test.shape)
            print("y_test shape:", y_test.shape)


            model_report:dict=evaluate_models(X_train, y_train, X_test, y_test, Models, params)
            best_model_score= max(sorted(model_report.values()))
            # to get best model name
            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model= Models[best_model_name]
            print("this is the best model")
            print(best_model_name)
            model_name=list(params.keys())
            actual_model = best_model_name if best_model_name in params else ""

            if actual_model:
               best_params = params[actual_model]
            else:
             raise CustomException("Best model not found in parameters.")


            mlflow.set_registry_uri("https://dagshub.com/DataWizard99/ML-projects.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # mlflow

            with mlflow.start_run():

                predicted_qualities = best_model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_params(best_params)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)


                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(best_model, "model", registered_model_name=actual_model)
                else:
                    mlflow.sklearn.log_model(best_model, "model")


            if best_model_score<0.6:
                raise CustomException("no best model found")
            logging.info(f"best founding model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square


        except Exception as e:
            raise CustomException(e,sys)

























