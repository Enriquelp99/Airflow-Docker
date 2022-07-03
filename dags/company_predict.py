from cmath import exp
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sqlalchemy import create_engine
from datetime import timedelta, datetime
import xgboost as xgb
from sklearn.metrics import roc_auc_score

default_args = {
    'owner':'Enrique Liebana Peña',
    'depends_on_the_past':False,
    'email':'enrique-liebana@outlook.com',
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':0,
    'retry_delay':timedelta(minutes=30)
}

def _load_model():
    alchemyEngine= create_engine('postgresql+psycopg2://airflow:airflow@postgres/data_company', pool_recycle=3600)
    dbConnection = alchemyEngine.connect()
    dataFrame = pd.read_sql("select * from company_P", dbConnection)
    X = dataFrame.drop('churn', axis=1)
    y = dataFrame.churn
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
    pickle_m = pickle.load(open('models/XGBoost_F.pkl', 'rb'))
    score = roc_auc_score(y_test, pickle_m.predict_proba(X_test)[:,1])
    acc = accuracy_score(y_test, pickle_m.predict(X_test))
    print("{:<15}| ROC-AUC score = {:.3f} | Accuracy = {:.3f}".format('XGBOOST', score, acc))


with DAG('Company_Predict', 
    schedule_interval=None, 
    default_args=default_args,
    start_date=datetime(2022,6,29)

) as dag:
    
    load_model = PythonOperator(
        task_id='load_Model',
        python_callable=_load_model
    )
    trigger_target = TriggerDagRunOperator(
            task_id='trigger_target',
            trigger_dag_id='SDG_Enrique_V0',
            execution_date='{{ ds }}',
            reset_dag_run=True,
            wait_for_completion=True,
)

trigger_target >> load_model