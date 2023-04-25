import pymongo
import traceback
import os
from dotenv import load_dotenv, find_dotenv
from registrar_logs.registrar_log import registrar_log

try:
	load_dotenv(find_dotenv(filename='config/.env'))

	HOSTS = os.environ.get("HOSTS")
	REPLICASET = os.environ.get("REPLICASET")
	KAFKA_USER = os.environ.get("KAFKA_USER")
	KAFKA_PASSWORD = os.environ.get("KAFKA_PASSWORD")
	DATABASE_MONGO = os.environ.get("DATABASE_MONGO")
	COLLECTION_MONGO = os.environ.get("COLLECTION_MONGO")

	registrar_log("Realizando conexão ao MongoDB")
	uri = f"mongodb://{KAFKA_USER}:{KAFKA_PASSWORD}@{HOSTS}/{DATABASE_MONGO}?replicaSet={REPLICASET}"
	mongo_client = pymongo.MongoClient(uri)

	registrar_log("Verificando o database")
	db = mongo_client.get_database()
	registrar_log(db.name)

	registrar_log(f"Conectando a collection {COLLECTION_MONGO}")
	col = db[COLLECTION_MONGO]

	registrar_log("Conexão ao MongoDB realizada")
except:
	registrar_log("Erro ao se conectar ao MongoDB")
	raise Exception(traceback.format_exc())