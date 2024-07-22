import sqlite3
import pandas as pd
import logging
from logging_config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

def extract_data():
    conn = sqlite3.connect('monitoring.db')
    query = '''
    SELECT dag_id, task_name, task_type, start_time, end_time, duration
    FROM monitoring
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    logger.debug(f"Extracted DataFrame: \n{df}")
    return df
