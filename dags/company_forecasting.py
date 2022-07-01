from datetime import datetime, timedelta
from pkgutil import read_code
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import logging 
from calendar import c
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score
from sqlalchemy import create_engine
import csv
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sklearn.model_selection import train_test_split
import csv
import pickle
from sqlalchemy import create_engine





def get_SQLSentence(dataframe,table):
    sentence = "CREATE TABLE IF NOT EXISTS " + table +"("
    for a in dataframe.columns:
        if dataframe.columns[-1] != a:
            sentence += str(a) + " " + str(dataframe[a].dtype) + ", \n"
        else:
            sentence += str(a) + " " + str(dataframe[a].dtype) + ");\n"    
    sentence = sentence.replace("float64", "REAL")
    sentence = sentence.replace("object","VARCHAR")
    sentence = sentence.replace("uint8","INT4")
    sentence = sentence.replace("int64","INT4")
    print(sentence) 
    return sentence  


def postgreSQL_getTable():
    pd.set_option('display.max_rows',150)
    pd.set_option('display.max_columns',150)
    hook = PostgresHook(postgres_conn_id="postgres_conection")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from company")
    with open(f"/raw_data/company.csv", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Backup Company data in : %s", f"/raw_data/company.csv")


def read_and_convertColumns():
    data_company = pd.read_csv('/raw_data/company.csv',delimiter=',',header=0)
    print(data_company.head())
    print(data_company.dtypes)
    print("**************** FLOAT COLUmNS *********************")
    col_float=['rev_mean','mou_mean','totmrc_mean','da_mean','ovrmou_mean','ovrrev_mean','vceovr_mean','datovr_mean','roam_mean','change_mou','change_rev','drop_vce_mean','drop_dat_mean','blck_vce_mean','blck_dat_mean','unan_vce_mean','unan_dat_mean','plcd_vce_mean','plcd_dat_mean','recv_vce_mean','recv_sms_mean','comp_vce_mean','comp_dat_mean','custcare_mean','ccrndmou_mean','cc_mou_mean','inonemin_mean','threeway_mean','mou_cvce_mean','mou_cdat_mean','mou_rvce_mean','owylis_vce_mean','mouowylisv_mean','iwylis_vce_mean','mouiwylisv_mean','peak_vce_mean','peak_dat_mean','mou_peav_mean','mou_pead_mean','opk_vce_mean','opk_dat_mean','mou_opkv_mean','mou_opkd_mean','drop_blk_mean','attempt_mean','complete_mean','callfwdv_mean','callwait_mean','totmou','totrev','adjrev','adjmou','avgrev','avgmou','avgqty','hnd_price']
    for a in col_float:
        data_company[a]=data_company[a].astype(str).str.replace(',', '.').astype(float)
    print(data_company[col_float].head())
    print("**************** OBJECT COLUmNS *********************")
    col_object = data_company.select_dtypes('object')
    data_company[col_object.columns] = data_company[col_object.columns].astype('string')
            
    print("************+***********RESULTS*****************************")
    print("FLOAT64",data_company.select_dtypes('float64').shape)
    print("INT64",data_company.select_dtypes('int').shape)
    print("STRING",data_company.select_dtypes('string').shape)
    print(data_company.head())
    data_company.to_csv("/processed_data/company_A01.csv",index=False)

    hook = PostgresHook(postgres_conn_id="postgres_conection")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS company_A01 (
        rev_mean REAL,
        mou_mean REAL,
        totmrc_mean REAL,
        da_mean REAL,
        ovrmou_mean REAL,
        ovrrev_mean REAL,
        vceovr_mean REAL,
        datovr_mean REAL,
        roam_mean REAL,
        change_mou REAL,
        change_rev REAL,
        drop_vce_mean REAL,
        drop_dat_mean REAL,
        blck_vce_mean REAL,
        blck_dat_mean REAL,
        unan_vce_mean REAL,
        unan_dat_mean REAL,
        plcd_vce_mean REAL,
        plcd_dat_mean REAL,
        recv_vce_mean REAL,
        recv_sms_mean REAL,
        comp_vce_mean REAL,
        comp_dat_mean REAL,
        custcare_mean REAL,
        ccrndmou_mean REAL,
        cc_mou_mean REAL,
        inonemin_mean REAL,
        threeway_mean REAL,
        mou_cvce_mean REAL,
        mou_cdat_mean REAL,
        mou_rvce_mean REAL,
        owylis_vce_mean REAL,
        mouowylisv_mean REAL,
        iwylis_vce_mean REAL,
        mouiwylisv_mean REAL,
        peak_vce_mean REAL,
        peak_dat_mean REAL,
        mou_peav_mean REAL,
        mou_pead_mean REAL,
        opk_vce_mean REAL,
        opk_dat_mean REAL,
        mou_opkv_mean REAL,
        mou_opkd_mean REAL,
        drop_blk_mean REAL,
        attempt_mean REAL,
        complete_mean REAL,
        callfwdv_mean REAL,
        callwait_mean REAL,
        churn REAL,
        months REAL,
        uniqsubs REAL,
        actvsubs REAL,
        new_cell VARCHAR,
        crclscod VARCHAR,
        asl_flag VARCHAR,
        totcalls REAL,
        totmou REAL,
        totrev REAL,
        adjrev REAL,
        adjmou REAL, 
        adjqty REAL,
        avgrev REAL,
        avgmou REAL,
        avgqty REAL,
        avg3mou REAL,
        avg3qty REAL,
        avg3rev REAL,
        avg6mou REAL,
        avg6qty REAL,
        avg6rev REAL,
        prizm_social_one VARCHAR,
        area VARCHAR,
        dualband VARCHAR,
        refurb_new VARCHAR,
        hnd_price REAL,
        phones VARCHAR,
        models REAL,
        hnd_webcap VARCHAR,
        truck REAL,
        rv REAL,
        ownrent  VARCHAR,
        lor REAL,
        dwlltype VARCHAR,
        marital VARCHAR,
        adults REAL,
        infobase  VARCHAR,
        income REAL,
        numbcars REAL,
        hhstatin  VARCHAR,
        dwllsize  VARCHAR,
        forgntvl REAL,
        ethnic  VARCHAR,
        kid0_2  VARCHAR,
        kid3_5  VARCHAR,
        kid6_10  VARCHAR,
        kid11_15  VARCHAR,
        kid16_17  VARCHAR,
        creditcd VARCHAR,
        eqpdays REAL,
        customer_id REAL
        );""")

    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    file = open('/processed_data/company_A01.csv', "r")
    table = 'company_A01'
    with conn.cursor() as cur:
        cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
        cur.copy_expert(sql=sql % table, file=file)
        conn.commit()
#         cur.close()
#         connection.close()
    cursor.close()
    conn.close()


def preprocessing():
    data_company = pd.read_csv('/processed_data/company_A01.csv',delimiter=',',header=0)

    col_float=['rev_mean','mou_mean','totmrc_mean','da_mean','ovrmou_mean','ovrrev_mean','vceovr_mean','datovr_mean','roam_mean','change_mou','change_rev','drop_vce_mean','drop_dat_mean','blck_vce_mean','blck_dat_mean','unan_vce_mean','unan_dat_mean','plcd_vce_mean','plcd_dat_mean','recv_vce_mean','recv_sms_mean','comp_vce_mean','comp_dat_mean','custcare_mean','ccrndmou_mean','cc_mou_mean','inonemin_mean','threeway_mean','mou_cvce_mean','mou_cdat_mean','mou_rvce_mean','owylis_vce_mean','mouowylisv_mean','iwylis_vce_mean','mouiwylisv_mean','peak_vce_mean','peak_dat_mean','mou_peav_mean','mou_pead_mean','opk_vce_mean','opk_dat_mean','mou_opkv_mean','mou_opkd_mean','drop_blk_mean','attempt_mean','complete_mean','callfwdv_mean','callwait_mean','totmou','totrev','adjrev','adjmou','avgrev','avgmou','avgqty','hnd_price']
    for a in col_float:
        data_company[a]=data_company[a].astype(str).str.replace(',', '.').astype(float) 

    print("**************** OBJECT COLUmNS *********************")
    col_object = data_company.select_dtypes('object')
    data_company[col_object.columns] = data_company[col_object.columns].astype('string')
    print(data_company.columns)
    data_company=data_company.drop(['customer_id'],axis=1)
    
    col_float = data_company.select_dtypes('float64').columns
    col_integer = data_company.select_dtypes('int64').columns
    col_categorical = data_company.select_dtypes('string').columns

    missing_data_percent =  100*data_company.isnull().sum()/len(data_company)
    missing_data_percent[missing_data_percent > 0].sort_values(ascending=False)
    col_missing_data_less_30_perc = missing_data_percent[missing_data_percent.le(30)].index
    data_company = data_company[col_missing_data_less_30_perc]

    def cap_outliers(array, k=3):
        upper_limit = array.mean() + k*array.std()
        lower_limit = array.mean() - k*array.std()
        array[array<lower_limit] = lower_limit
        array[array>upper_limit] = upper_limit
        return array

    data_company[data_company.describe().columns] = data_company[data_company.describe().columns].apply(cap_outliers, axis=0)

    print(data_company.shape)

    col_categorical = [x for x in col_categorical if x in data_company.columns]
    data_company[col_categorical].isnull().sum()
    data_company[col_categorical]=data_company[col_categorical].fillna('U')
    col_OneHot = [x for x in col_categorical if len(data_company[x].value_counts())  > 2 and len(data_company[x].value_counts() < 25 )]
    col_categorical = [x for x in col_categorical if x not in col_OneHot]
    
    print(data_company.shape)
    a = data_company[col_categorical].isnull().sum()
    col_DROP = [x for x in range(len(a)) if a[x] > 5000]
    col_DROP_Names = [a[col_DROP].index[i] for i in range(len(a[col_DROP].index))]
    print(col_DROP_Names)
    data_company = data_company.drop(col_DROP_Names,axis=1)

    print(data_company.shape)
    col_categorical = [x for x in col_categorical if x not in col_DROP_Names]
    data_company = data_company.dropna(subset=col_categorical,axis=0)
    print(data_company.shape)

    LEncoder = LabelEncoder()
    data_company[col_categorical].describe
    for col in col_categorical:
        data_company[col] = LEncoder.fit_transform(data_company[col]).astype(int)

    data_company['area'] = LEncoder.fit_transform(data_company['area']).astype(int)

    print(data_company[col_categorical].describe)

    for col in col_OneHot:
        dummy = pd.get_dummies(data_company[col],prefix=col)
        data_company = data_company.join(dummy)
        data_company = data_company.drop(col,axis=1)

    data_company.shape
    col_float = data_company.select_dtypes('float64').columns
    col_integer = data_company.select_dtypes('int64').columns

    impute_cols = data_company.columns[data_company.isnull().sum() > 1]
    print(impute_cols)

    from sklearn.impute import SimpleImputer
    imp = SimpleImputer(strategy='median', fill_value=0)
    data_company[impute_cols] = imp.fit_transform(data_company[impute_cols])
    a = data_company[col_float].isnull().sum()
    col_DROP2 = [x for x in range(len(a)) if a[x] > 5000]
    col_DROP_Names2 = [a[col_DROP2].index[i] for i in range(len(a[col_DROP2].index))]
    data_company = data_company.drop(col_DROP_Names2,axis=1)
    data_company.shape

    corr = data_company.corr()
    columns = np.full((corr.shape[0],), True, dtype=bool)
    for i in range (corr.shape[0]):
        for j in range(i+1, corr.shape[0]):
            if corr.iloc[i,j] >= 0.90:
                if columns[j]:
                    columns[j]=False
    col_corr=list()
    for i in range(0,len(columns)):
        if columns[i] == True:
            col_corr.append(data_company.columns[i])
            
    columns_notcorr = [x for x in data_company.columns if x not in col_corr]

    data_company=data_company.drop(columns=columns_notcorr)
    col_float = [x for x in col_float if x in col_corr]
    print(data_company.columns)

    data_company = data_company.dropna()

    data_company.to_csv("/processed_data/company_A02.csv",index=False)

    hook = PostgresHook(postgres_conn_id="postgres_conection")
    conn = hook.get_conn()
    cursor = conn.cursor()
    company_A02 = get_SQLSentence(data_company,'company_A02')
    cursor.execute("DROP TABLE IF EXISTS company_A02")
    cursor.execute(company_A02)
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    
    file = open('/processed_data/company_A02.csv', "r")
    table = 'company_A02'
    with conn.cursor() as cur:
        cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
        cur.copy_expert(sql=sql % table, file=file)
        conn.commit()

    cursor.close()
    conn.close()


def _feature_Selection():
    data_company = pd.read_csv('processed_data/company_A02.csv',delimiter=',',header=0)
    target0 = data_company['churn'] # for y
    features0   = data_company.drop(['churn'], axis=1) # for X
    feature_model = pickle.load(open('models/dTree_FeatureSelection.sav', 'rb'))
    data_Features = data_company.drop('churn',axis=1)
    data_Features = data_Features.loc[:,feature_model]
    data=data_Features.join(data_company['churn'])
    
    data.to_csv("/processed_data/company_P.csv",index=False)

    hook = PostgresHook(postgres_conn_id="postgres_conection")
    conn = hook.get_conn()
    cursor = conn.cursor()
    company_P = get_SQLSentence(data,'company_P')
    cursor.execute("DROP TABLE IF EXISTS company_P")
    cursor.execute(company_P)
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    
    file = open('/processed_data/company_P.csv', "r")
    table = 'company_P'
    with conn.cursor() as cur:
        cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
        cur.copy_expert(sql=sql % table, file=file)
        conn.commit()

    cursor.close()

default_args={
    'owner':'Enrique Liebana Peña',
    'depends_on_the_past':False,
    'email':'enrique-liebana@outlook.com',
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':0,
    'retry_delay':timedelta(minutes=30)
}

with DAG(
    dag_id='SDG_Enrique_V0',
    default_args=default_args,
    description='SDGProject',
    start_date=datetime(2022,6,29),
    tags=['SDG Group','EDA','PostgreSQL'],
    schedule_interval='@daily',
    
) as dag:
    init_config = PythonOperator(task_id="postgreSQL_getTable",python_callable=postgreSQL_getTable)
    read_Convert = PythonOperator(task_id="readCSV_convertColumns",python_callable=read_and_convertColumns)
    preprocessing_data = PythonOperator(task_id="preprocessing_data",python_callable=preprocessing)
    feature_Selection = PythonOperator(task_id="Feature_Selection",python_callable=_feature_Selection)

    init_config >> read_Convert >> preprocessing_data >> feature_Selection