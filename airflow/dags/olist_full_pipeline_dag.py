from __future__ import annotations

import sys
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# --- الخطوة 1: إضافة مسار المشروع إلى مسار بايثون ---
# هذا يسمح لـ Airflow بالعثور على السكربت الخاص بك في مجلد "scripts"
sys.path.append('/opt/airflow/projects/Olist_ETL_Project')
from scripts.ingest_to_bronze import main_ingest

# --- تعريف الـ DAG ---
with DAG(
    dag_id='olist_end_to_end_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['olist', 'dbt'],
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
) as dag:

    # --- المهمة الأولى: تشغيل سكربت بايثون لتحميل البيانات الخام ---
    ingest_task = PythonOperator(
        task_id='ingest_raw_data_to_bronze',
        python_callable=main_ingest
    )

    # --- تعريف المسار إلى مشروع dbt داخل الحاوية ---
    dbt_project_path = "/opt/airflow/projects/Olist_ETL_Project/dbt_project/olist_dbt_project/"

    # --- المهمة الثانية: تشغيل dbt لبناء كل النماذج ---
    dbt_run_task = BashOperator(
        task_id='run_dbt_models',
        bash_command=f"cd {dbt_project_path} && dbt run"
    )

    # --- المهمة الثالثة: تشغيل اختبارات الجودة ---
    dbt_test_task = BashOperator(
        task_id='test_dbt_models',
        bash_command=f"cd {dbt_project_path} && dbt test"
    )

    # --- تحديد ترتيب تنفيذ المهام ---
    ingest_task >> dbt_run_task >> dbt_test_task