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
    --IP)
    IP="$2"
    shift
    ;;
    *)
    # desconhecido
    ;;
esac
shift
done

echo -e 'Cria um hostname para o IP da máquina host'

if grep -q "masterkub" /etc/hosts; then
    echo -e "O arquivo /etc/hosts já contém a entrada $IP   masterkub"
else
    sudo echo "$IP   masterkub" >> /etc/hosts
    echo -e "A entrada $IP   masterkub foi adicionada ao arquivo /etc/hosts"
fi

echo -e 'Construindo imagem python para consumir dados do Kafka'
docker image rm masterkub:5000/python-image:latest python-image:latest
docker build . -t python-image
echo -e 'Enviando imagem python para registry local'
docker-compose up -d
docker tag python-image:latest masterkub:5000/python-image:latest
docker push masterkub:5000/python-image:latest
echo -e 'Criando Pods Kubernetes'
kubectl apply -f kub-teste.yml
echo -e 'Realizando pausa de 200 segundos'
sleep 200
echo -e 'Criando topico responsável por toda ingestao de dados'
kubectl exec -it $(kubectl get pods -n kafka | grep kafkazoo | awk '{print $1}') -c kafka1 -n kafka -- /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topico1" --bootstrap-server localhost:9092 -replication-factor 2 --partitions 1 --command-config /opt/bitnami/kafka/config/kafka_client_jaas.conf
echo -e 'Criando topico usado para conferência de Ids'
kubectl exec -it $(kubectl get pods -n kafka | grep kafkazoo | awk '{print $1}') -c kafka1 -n kafka -- /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topico2" --bootstrap-server localhost:9092 -replication-factor 2 --partitions 1 --command-config /opt/bitnami/kafka/config/kafka_client_jaas.conf
echo -e 'Monta cluster MongoDB, cria database, collection e usuario'
kubectl exec -it $(kubectl get pods -n kafka | grep mongopod | awk '{print $1}') -c mongo -n kafka -- chmod +x /rs-init.sh
kubectl exec -it $(kubectl get pods -n kafka | grep mongopod | awk '{print $1}') -c mongo -n kafka -- chmod +x /init.js
kubectl exec -it $(kubectl get pods -n kafka | grep mongopod | awk '{print $1}') -c mongo -n kafka -- /bin/bash -c "/rs-init.sh"