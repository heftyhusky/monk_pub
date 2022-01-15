import os

MYSQL_DATA_HOST = os.environ.get("MYSQL_DATA_HOST", "mysqldb")
MYSQL_DATA_USER = os.environ.get("MYSQL_DATA_USER", "root")
MYSQL_DATA_PASSWORD = os.environ.get("MYSQL_DATA_PASSWORD", "1123")
MYSQL_DATA_DATABASE = os.environ.get("MYSQL_DATA_DATABASE", "healthData")
MYSQL_DATA_PORT = int(os.environ.get("MYSQL_DATA_PORT", "3306"))

WORKER_ACCOUNT = os.environ.get("WORKER_ACCOUNT", "worker")
WORKER_PASSWORD = os.environ.get("WORKER_PASSWORD", "worker")

MESSAGE_QUEUE_HOST = os.environ.get("MESSAGE_QUEUE_HOST", "rabbitmq")
MESSAGE_QUEUE_PORT = int(os.environ.get("MESSAGE_QUEUE_PORT", "5672"))
