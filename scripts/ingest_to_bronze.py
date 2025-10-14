import os
import sys
import pandas as pd
from sqlalchemy import create_engine
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path
import logging
from dotenv import load_dotenv

# Ensure the project root is in the path to import config
# This makes the script runnable from anywhere
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from config import PG_CONFIG, SNOWFLAKE_CONFIG

# Load environment variables from .env file
load_dotenv()

# --- Setup professional logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main_ingest():
    """
    Main function to extract data from all sources (PostgreSQL & CSVs)
    and load it into the Snowflake Bronze layer.
    """
    
    conn_sf = None  # Initialize connection to None
    try:
        # --- Connect to Snowflake ---
        # Add role to Snowflake config for correct permissions
        snowflake_config_with_role = SNOWFLAKE_CONFIG.copy()
        snowflake_config_with_role['role'] = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
        
        conn_sf = snowflake.connector.connect(**snowflake_config_with_role)
        logging.info("✅ Connected to Snowflake successfully")

        # --- Extract from PostgreSQL ---
        logging.info("=" * 20 + " Starting PostgreSQL Ingestion " + "=" * 20)
        pg_engine = create_engine(
            f'postgresql://{PG_CONFIG["user"]}:{PG_CONFIG["password"]}@{PG_CONFIG["host"]}:{PG_CONFIG["port"]}/{PG_CONFIG["database"]}'
        )
        pg_tables = ['raw_customers', 'raw_orders']

        for table in pg_tables:
            logging.info(f"Reading table: {table} from PostgreSQL...")
            df = pd.read_sql(f'SELECT * FROM {table}', pg_engine)
            logging.info(f"Loaded {len(df):,} rows from {table}")
            
            # Use lowercase with quoting for consistency
            table_name_sf = table.lower()
            logging.info(f"Writing to Snowflake table: {table_name_sf}...")
            write_pandas(conn_sf, df, table_name_sf)
            logging.info(f"✓ Successfully wrote {table_name_sf} to Snowflake")

        # --- Extract from CSV files ---
        logging.info("=" * 20 + " Starting CSV Ingestion " + "=" * 20)
        csv_path = project_root / 'data' / 'raw_data'
        
        if not csv_path.exists():
            raise FileNotFoundError(f"Critical error: CSV directory not found at {csv_path}")

        csv_files = [
            f for f in os.listdir(csv_path) 
            if f.endswith('.csv') 
            and 'customers' not in f 
            and 'orders' not in f
        ]
        
        logging.info(f"Found {len(csv_files)} CSV files to process.")

        for file in csv_files:
            logging.info(f"Reading file: {file}...")
            df = pd.read_csv(csv_path / file)
            logging.info(f"Loaded {len(df):,} rows from {file}")
            
            # Generate a clean, lowercase table name
            table_name_sf = "raw_" + os.path.splitext(file)[0]\
                .replace('olist_', '')\
                .replace('_dataset', '')
            
            logging.info(f"Writing to Snowflake table: {table_name_sf}...")
            write_pandas(conn_sf, df, table_name_sf)
            logging.info(f"✓ Successfully wrote {table_name_sf} to Snowflake")

    except Exception as e:
        logging.error(f"❌ An error occurred during the ingestion process: {e}")
        # Raise the exception to make the Airflow task fail
        raise
    finally:
        # --- This block ensures the connection is always closed ---
        if conn_sf:
            conn_sf.close()
            logging.info("Snowflake connection closed.")
    
    logging.info("=" * 50)
    logging.info("✅✅✅ Ingestion process completed successfully! ✅✅✅")
    logging.info("=" * 50)


if __name__ == '__main__':
    main_ingest()