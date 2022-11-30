import os
from dotenv import load_dotenv

# load_dotenv(r'C:\Users\Kirill\Desktop\final_project\.env')
# SELENOID_NAME = 'localhost'
SELENOID_NAME = os.getenv('SELENOID_NAME')
SELENOID_PORT = os.getenv('SELENOID_PORT')

# APP_NAME = 'localhost'
APP_NAME = os.getenv('APP_NAME')
APP_PORT = os.getenv('APP_PORT')

USER_NAME = os.getenv('USER_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')

# MYSQL_NAME = 'localhost'
MYSQL_NAME = os.getenv('MYSQL_NAME')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# MOCK_HOST = '127.0.0.1'
MOCK_HOST = os.getenv('MOCK_HOST')
MOCK_PORT = os.getenv('MOCK_PORT')
