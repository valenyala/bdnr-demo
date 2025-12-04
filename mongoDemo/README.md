# MongoDB ReplicaSet + Transactions Demo

## Prerequisitos:
- Instalar Docker y Docker compose
- Instalar python y venv o Anaconda (para crear entornos virtuales)

Para esta demo se usará Anaconda.

## Setup del environment:

ejecutar en la terminal:
```
conda create -n mongo-demo
conda activate mongo-demo
conda install pymongo
```

### Mac/Linux:
Editar /etc/hosts:
```
sudo nano /etc/hosts
```

Agregar:
`127.0.0.1   mongo1 mongo2 mongo3`
Guardar y salir

### Windows:
Editar el archivo C:\Windows\System32\drivers\etc\hosts con permisos del administrador y agregar las siguientes lineas: 
```
127.0.0.1   mongo1
127.0.0.1   mongo2
127.0.0.1   mongo3
```
Guardar

## Levantar los contenedores e inicializar el Replicaset
```
docker compose up -d
```
### Mac/Linux:
```
./start-replica.sh
```
### Windows:
./start-replica.bat

# Ejecutar la demo en Python
Con el ambiente mongo-demo activado:
```
python demo.py
```

# Apagar el environment
```bash
# Parar servicios
docker-compose down

# Borrar volúmenes (datos persistentes)
docker-compose down -v

# Borrar todo (imágenes incluidas)
docker-compose down -v --rmi all
conda deactivate
```
Y eliminar las lineas agregadas en el archivo host
