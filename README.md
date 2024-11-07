## end to end data science projects##
MLFLOW_TRACKING_URI= https://dagshub.com/DataWizard99/ML-projects.mlflow \
MLFLOW_TRACKING_USERNAME=DataWizard99 \
MLFLOW_TRACKING_PASSWORD=aa7a444bd1464eedb451e46a312d75be54ef6679 \
python script.py
import dagshub
dagshub.init(repo_owner='DataWizard99', repo_name='ML-projects', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)