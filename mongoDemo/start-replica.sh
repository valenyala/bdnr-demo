#!/bin/bash

echo "Inicializando replica set..."
docker exec -it mongo1 mongosh --eval '
  rs.initiate({
    _id: "rs0",
    members: [
      {_id: 0, host: "mongo1:27017", priority: 2},
      {_id: 1, host: "mongo2:27017", priority: 1},
      {_id: 2, host: "mongo3:27017", priority: 1}
    ]
  })
'

echo "Esperando elección de PRIMARY..."
sleep 10

echo "Verificando estado del cluster:"
docker exec -it mongo1 mongosh --eval 'rs.status().members.forEach(m => print(m.name + " - " + m.stateStr))'

echo "
Replica set listo!
PRIMARY será mongo1 (prioridad 2)
Conexión: mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0
"
