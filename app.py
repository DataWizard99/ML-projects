import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from mlproject.logger import logging  # Now this should work
from mlproject.exception import CustomException
from mlproject.components.data_ingestion import DataIngestion
from mlproject.components.data_ingestion import DataIngestionConfig
from mlproject.components.data_transformation import DataTransformationConfig, DataTransformation
if __name__=="__main__":
    logging.info("the execution has started")


    try:
        # data_ingestion_config= DataIngestionConfig()
        data_ingestion= DataIngestion()
        train_data_path, test_data_path=data_ingestion.initiate_data_ingestion()
        data_transformation=DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

    except Exception as e:
        logging.info('Custom Exception')
        raise CustomException(e, sys)