import os
import traceback
from registrar_logs.registrar_log import registrar_log
from dotenv import load_dotenv, find_dotenv
from kafka import KafkaConsumer

try:
	load_dotenv(find_dotenv(filename='config/.env'))

	BOOTSTRAP_SERVERS = os.environ.get("BOOTSTRAP_SERVERS")
	SASL_USER = os.environ.get("SASL_USER")
	SASL_PASSWORD = os.environ.get("SASL_PASSWORD")
	SSL_PASSWORD = os.environ.get("SSL_PASSWORD")

	bootstrap_servers_list = BOOTSTRAP_SERVERS.split(',')
	topico = os.environ.get("TOPICO_CONSUMER")

	registrar_log("Realizando conexão ao Kafka Consumer")
	consumer = KafkaConsumer(
		bootstrap_servers=bootstrap_servers_list,
		security_protocol='SASL_SSL',
		sasl_mechanism='PLAIN',
		sasl_plain_username=SASL_USER,
		sasl_plain_password=SASL_PASSWORD,
		ssl_cafile='config/CARoot.pem',
		ssl_certfile='config/ca-cert',
		ssl_keyfile='config/ca-key',
		ssl_password=SSL_PASSWORD,
		ssl_check_hostname=False
	)

	registrar_log("Conexão ao Kafka Consumer realizada")
except:
	registrar_log("Erro ao se conectar ao Kafka Consumer")
	raise Exception(traceback.format_exc())
