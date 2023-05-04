while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --topico1)
    topico1="$2"
    shift
    ;;
    --topico2)
    topico2="$2"
    shift
    ;;
    --mongo1)
    mongo1="$2"
    shift
    ;;
    --mongo2)
    mongo2="$2"
    shift
    ;;
    --mongo3)
    mongo3="$2"
    shift
    ;;
    *)
    # desconhecido
    ;;
esac
shift
done

docker-compose up -d
echo -e 'Realizando pausa de 200 segundos'
sleep 200
echo -e 'Criando topico responsável por toda ingestao de dados'
docker exec kafka1 /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topico1" --bootstrap-server localhost:9092 -replication-factor 2 --partitions 1 --command-config /opt/bitnami/kafka/config/kafka_client_jaas.conf
echo -e 'Criando topico usado para conferência de Ids'
docker exec kafka1 /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topico2" --bootstrap-server localhost:9092 -replication-factor 2 --partitions 1 --command-config /opt/bitnami/kafka/config/kafka_client_jaas.conf
echo -e 'Monta cluster MongoDB, cria database, collection e usuario'
docker exec mongodb chmod +x /rs-init.sh
docker exec mongodb chmod +x /init.js
docker exec mongodb /bin/bash -c "/rs-init.sh --mongo1 $mongo1 --mongo2 $mongo2 --mongo3 $mongo3"


