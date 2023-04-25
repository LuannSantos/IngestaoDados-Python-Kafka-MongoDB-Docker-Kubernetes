import requests
import json
import traceback
from time import sleep 

import conecta_kafka_producer.conecta_kafka_producer as kp
import conecta_kafka_consumer.conecta_kafka_consumer as kc
from registrar_logs.registrar_log import registrar_log


def realiza_leitura_dados(max_id, num_tentativas):

	try:
		registrar_log("Verifica quantidade total de artigos")
		url = 'https://api.spaceflightnewsapi.net/v3/articles/count'
		resp_count_articles = requests.get(url)

		registrar_log(f"Pesquisa artigos com id mínimo {max_id}")

		url = f'https://api.spaceflightnewsapi.net/v3/articles?_limit={int(resp_count_articles.text)}&id_gt={max_id}&_sort=id'
		resp_articles = requests.get(url)
		articles = resp_articles.json()

		articles_list = [articles] if type(articles) == "<class 'dict'>" else articles

		registrar_log(f"Quantidade de artigos encontrados: {len(articles_list)}")
	except:
		registrar_log("Erro ao tentar acessar a API")
		registrar_log(traceback.format_exc())

	try:
		registrar_log("Envia dados para o producer do kafka")
		for art in articles_list:
			id_art = art["id"]
			registrar_log(f"Envia artigo com id, {id_art}")
			max_id = id_art
			article_text = json.dumps(art)
			kp.producer.send(kp.topico, value = article_text.encode())
			kp.producer.flush()

			registrar_log(f"Salva novo valor de id máximo {max_id}")
			with open("max_id.txt", "w") as arquivo:
				arquivo.write(str(max_id))
				arquivo.close()

			sleep(0.3)

		registrar_log("Dados enviados para o producer")
		num_tentativas = 0
	except:
		num_tentativas += 1
		registrar_log("Erro ao tentar enviar dados ao producer")
		registrar_log(traceback.format_exc())

	return max_id, num_tentativas

def obtem_id_maximo():
	max_id = 0
	kc.consumer.subscribe([kc.topico])
	for message in kc.consumer:
		max_id_str = message.value.decode()
		max_id = int(max_id_str)
		if (max_id > 0 ):
			break

	return max_id


if __name__ == "__main__":

	num_tentativas = 0
	registrar_log("Inicio do código que realizará a produção de mensagens")
	registrar_log("Verifica valor máximo de id gravado localmente")
	try:
		with open("max_id.txt", "r") as arquivo:
			max_id = arquivo.read()
	except:
		registrar_log("Erro ao ler valor atual de id máximo")
		raise Exception(traceback.format_exc())

	while num_tentativas < 11:
		registrar_log(f"Realiza leitura de dados da API. O Id máximo que será usado no ínicio {max_id}")
		max_id, num_tentativas = realiza_leitura_dados(max_id, num_tentativas)
		max_id_consumer = obtem_id_maximo()
		max_id = max_id if max_id < max_id_consumer else max_id_consumer
		sleep(60)

	registrar_log("Processo encerrado devido ao alto número de tentativas mal sucedidas")

