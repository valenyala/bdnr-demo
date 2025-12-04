docker exec -it mongo1 mongosh --eval 'rs.status().members.forEach(m => print(m.name + " - " + m.stateStr))'
