import os

DB_DIALECT = 'mysql'
DB_DRIVER = 'pymysql'
DB_HOST = ''
DB_PORT = ''
DB_USER = 'admin'
DB_PASS = ''
DB_NAME = 'restaurantmenu'

SESSION_SECRET = 'temptest[kboitbot4og9504ng59es#Vn#gwn&]'

APP_HOST = '0.0.0.0'
APP_PORT = 8080

FLASK_ENABLE_DEBUG = True


if 'RDS_HOSTNAME' in os.environ:
    DB_HOST = os.environ['RDS_HOSTNAME']
    DB_PORT = os.environ['RDS_PORT']
    DB_USER = os.environ['RDS_USERNAME']
    DB_PASS = os.environ['RDS_PASSWORD']
    DB_NAME = os.environ['RDS_DB_NAME']