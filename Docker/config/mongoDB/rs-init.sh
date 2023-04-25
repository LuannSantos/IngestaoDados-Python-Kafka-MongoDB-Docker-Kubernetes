while [[ $# -gt 0 ]]
do
key="$1"
case $key in
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


mongosh <<EOF
var config = {
    "_id": "rs0",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "${mongo1}",
            "priority": 3
        },
        {
            "_id": 2,
            "host": "${mongo2}",
            "priority": 2       
        },
        {
            "_id": 3,
            "host": "${mongo3}",
            "priority": 1
        }
    ]
};
rs.initiate(config);
rs.reconfig(config, { force: true });
EOF

echo -e 'Realiza pausa de 120 segundos'
sleep 120

mongosh < /init.js
