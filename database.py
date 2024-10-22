import json
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from helper.json_helper import JsonHelper


# fungsi untuk membaca konfigurasi dari config.json
# def load_config():
#     with open('config.json', 'r') as file:
#         return json.load(file)



# memuat konfigurasi dari file JSON
json_helper = JsonHelper()
config = json_helper.load_config('config.json', 'r')

def get_connection_string(database_config_name):
    db_config = config['database'][database_config_name]
    return (
        f"DRIVER={{{db_config['driver']}}};"
        f"TrustServerCertificate=yes;"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['uid']};"
        f"PWD={db_config['pwd']};"
    )

# Connection strings
SQLALCHEMY_DATABASE_URL = URL.create("mssql+pyodbc", query={"odbc_connect": get_connection_string("raw_data")})
SQLALCHEMY_DATABASE_URL1 = URL.create("mssql+pyodbc", query={"odbc_connect": get_connection_string("clean_data")})
SQLALCHEMY_DATABASE_URL2 = URL.create("mssql+pyodbc", query={"odbc_connect": get_connection_string("warehouse_data")})

# Create engines
engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine1 = create_engine(SQLALCHEMY_DATABASE_URL1)
engine2 = create_engine(SQLALCHEMY_DATABASE_URL2)

# Create session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

Base = declarative_base()
Base1 = declarative_base()
Base2 = declarative_base()

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
    print("Database 'RAW_DATA' created success")

if not database_exists(SQLALCHEMY_DATABASE_URL1):
    create_database(SQLALCHEMY_DATABASE_URL1)
    print("Database 'CLEAN_DATA' created success")

if not database_exists(SQLALCHEMY_DATABASE_URL2):
    create_database(SQLALCHEMY_DATABASE_URL2)
    print("Database 'WAREHOUSE_DATA' created success")