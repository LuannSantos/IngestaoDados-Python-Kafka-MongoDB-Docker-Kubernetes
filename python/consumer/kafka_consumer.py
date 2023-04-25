import json
import traceback
from time import sleep 

from registrar_logs.registrar_log import registrar_log

registrar_log("Aguarda 600 segundos para inicializar todos os containers")
sleep(600)

import conecta_kafka_producer.conecta_kafka_producer as kp
import conecta_kafka_consumer.conecta_kafka_consumer as kc
import conecta_mongo.conecta_mongo as conn

def envia_id_maximo_producer():
	max_id = conn.db.col_articles.aggregate([{"$group": {"_id": None, "max_id": {"$max": "$id"}}}]).next()['max_id']
	registrar_log(f"Id máximo encontrado, {max_id}")
	kp.producer.send(kp.topico, value = str(max_id).encode()) 
	kp.producer.flush()


def artigo_nao_armazenado (id_artigo):
	query = {"id": id_artigo}

	results = conn.col.find(query)

	if len(list(results)) > 0:
		return False
	else:
		return True

def obtem_dados_consumer(num_tentativas):
	num_messages = 0
	try:
		registrar_log(f"Se inscreve no topico {kc.topico}")
		kc.consumer.subscribe([kc.topico])
		for message in kc.consumer:
			num_messages += 1
			message_json = json.loads(message.value.decode())
			id_message = message_json["id"]

			registrar_log(f"Dado obtido do consumer. Id: {id_message}")
			registrar_log("Verifica se artigo já existe no MongoDB")

			if (artigo_nao_armazenado(id_message)):
				registrar_log("Armazena artigo no MongoDB")
				result = conn.col.insert_one(message_json)
				registrar_log(f"Id gerado pelo MongoDB {result.inserted_id}")
			else:
				registrar_log("Artigo já armazenado no MongoDB")

			if (num_messages % 10 == 0):
				registrar_log("Envia id máximo para o producer")
				envia_id_maximo_producer()
				num_tentativas = 0
	except:
		num_tentativas += 1
		registrar_log("Erro ao tentar obter dados do consumer")
		registrar_log(traceback.format_exc())

	return num_tentativas



if __name__ == "__main__":

	num_tentativas = 0

	while num_tentativas < 5:
		registrar_log("Obtém dados do consumer")
		num_tentativas = obtem_dados_consumer(num_tentativas)


	registrar_log("Processo encerrado devido ao alto número de tentativas mal sucedidas")



