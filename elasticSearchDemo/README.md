# Foros Duolingo - Implementación con Elasticsearch

Implementación del subsistema de Foros y Comunidad usando Elasticsearch como fuente de verdad única.

**Elasticsearch Cluster:**
- 3 nodos para alta disponibilidad
- Sharding: threads (3), posts (5), reactions (3), reports (2)
- Réplicas: 1 por índice
- Refresh interval: 5s (near real-time)

## Prerequisitos:
- Instalar Docker y Docker compose
## Setup del environment:

ejecutar en la terminal:


## Instalación y configuración

### Levantar el cluster

```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar estado
docker-compose ps

# Logs (opcional)
docker-compose logs -f elasticsearch-node1
```

**Tiempo de inicio:** ~60 segundos hasta que el cluster esté listo.

### Verificar salud del cluster

```bash
# Esperar a que esté verde/amarillo
curl "http://localhost:9200/_cluster/health?pretty"

# Verificar nodos
curl "http://localhost:9200/_cat/nodes?v"
```

### Crear índices

```bash
./01-create-indices.sh
```

**Salida esperada:**
```
✅ Elasticsearch está listo
Creando índice forum_threads...
{"acknowledged":true,"shards_acknowledged":true,"index":"forum_threads"}
...
✅ Todos los índices creados exitosamente
```

### Insertar datos de prueba

```bash
./02-seed-data.sh
```

**Datos insertados:**
- 3 threads (español, inglés, francés)
- 5 posts visibles + 1 post spam oculto
- 2 reacciones
- 2 reportes (resueltos)

## Pruebas y demostración

### Búsquedas básicas

```bash
# Ejecutar suite completa de búsquedas
./search-examples.sh

# Resultados:
# 1. Búsqueda full-text
# 2. Listado por sección
# 3. Posts paginados
# 4. Top threads populares
# 5. Búsqueda por idioma/tags
# 6. Posts más útiles
# 7. Agregaciones por idioma
# 8. Autocompletado
```

### Moderación

```bash
# Ejecutar ejemplos de moderación
./moderation-examples.sh

# Resultados:
# 1. Reportes pendientes
# 2. Posts más reportados
# 3. Ocultar posts
# 4. Posts ocultos
# 5. Usuarios reportados
# 6. Resolver reportes
# 7. Distribución por razón
# 8. Actividad moderadores
```

### Queries manuales con curl

```bash
# Buscar todos los threads
curl "http://localhost:9200/forum_threads/_search?pretty"

# Buscar posts de un hilo
curl -X GET "http://localhost:9200/forum_posts/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"term": {"thread_id": "thread_001"}}}'

# Contadores
curl http://localhost:9200/_cat/count/forum_*?v
```

### Verificar performance

```bash
# Latencia de búsqueda
curl -X GET "http://localhost:9200/forum_posts/_search?pretty" \
  -w "\nTime: %{time_total}s\n" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match_all": {}}}'

# Estadísticas del índice
curl "http://localhost:9200/forum_posts/_stats?pretty"

# Salud de shards
curl "http://localhost:9200/_cat/shards/forum_*?v"
```

## Limpieza

```bash
# Parar servicios
docker-compose down

# Borrar volúmenes (datos persistentes)
docker-compose down -v

# Borrar todo (imágenes incluidas)
docker-compose down -v --rmi all
```

**Comandos útiles:**
```bash
# Listar todos los índices
curl http://localhost:9200/_cat/indices?v

# Ver mapping de un índice
curl http://localhost:9200/forum_posts/_mapping?pretty

# Analizar query performance
curl -X GET "http://localhost:9200/forum_posts/_search?explain=true" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match": {"content": "test"}}}'
```

```bash
# Test completo
./search-examples.sh && ./moderation-examples.sh && echo "TODO OK"
```
