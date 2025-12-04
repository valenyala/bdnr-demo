#!/bin/bash

ES_HOST="http://localhost:9200"

echo "Esperando a que Elasticsearch esté listo..."
until curl -s "$ES_HOST/_cluster/health" > /dev/null; do
    echo "Esperando..."
    sleep 2
done

echo "Elasticsearch está listo"

# Índice: forum_threads
echo "Creando índice forum_threads..."
curl -X PUT "$ES_HOST/forum_threads" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "5s",
    "analysis": {
      "analyzer": {
        "spanish_analyzer": {
          "type": "standard",
          "stopwords": "_spanish_"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "thread_id": {
        "type": "keyword"
      },
      "section": {
        "properties": {
          "section_id": {"type": "keyword"},
          "section_name": {"type": "keyword"}
        }
      },
      "title": {
        "type": "text",
        "analyzer": "spanish_analyzer",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      },
      "author": {
        "properties": {
          "user_id": {"type": "keyword"},
          "username": {"type": "keyword"},
          "display_name": {"type": "text"}
        }
      },
      "language": {
        "type": "keyword"
      },
      "tags": {
        "type": "keyword"
      },
      "state": {
        "type": "keyword"
      },
      "pinned": {
        "type": "boolean"
      },
      "locked": {
        "type": "boolean"
      },
      "statistics": {
        "properties": {
          "post_count": {"type": "integer"},
          "view_count": {"type": "integer"},
          "reaction_count": {"type": "integer"},
          "last_post_at": {"type": "date"}
        }
      },
      "created_at": {
        "type": "date"
      },
      "updated_at": {
        "type": "date"
      },
      "last_activity_at": {
        "type": "date"
      }
    }
  }
}'

echo ""

# ÍNDICE: forum_posts
echo "Creando índice forum_posts..."
curl -X PUT "$ES_HOST/forum_posts" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 1,
    "refresh_interval": "5s",
    "analysis": {
      "analyzer": {
        "multilang_analyzer": {
          "type": "standard",
          "stopwords": ["_spanish_", "_english_"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "post_id": {
        "type": "keyword"
      },
      "thread_id": {
        "type": "keyword"
      },
      "thread_title": {
        "type": "text",
        "index": false
      },
      "author": {
        "properties": {
          "user_id": {"type": "keyword"},
          "username": {"type": "keyword"},
          "display_name": {"type": "text"}
        }
      },
      "content": {
        "type": "text",
        "analyzer": "multilang_analyzer"
      },
      "language": {
        "type": "keyword"
      },
      "position": {
        "type": "integer"
      },
      "state": {
        "type": "keyword"
      },
      "reactions": {
        "properties": {
          "like": {"type": "integer"},
          "helpful": {"type": "integer"},
          "love": {"type": "integer"},
          "total": {"type": "integer"}
        }
      },
      "edit_history": {
        "type": "nested",
        "properties": {
          "content": {"type": "text", "index": false},
          "edited_at": {"type": "date"},
          "edited_by": {"type": "keyword"}
        }
      },
      "moderation": {
        "properties": {
          "hidden_reason": {"type": "keyword"},
          "hidden_at": {"type": "date"},
          "hidden_by": {"type": "keyword"},
          "moderator_notes": {"type": "text"}
        }
      },
      "created_at": {
        "type": "date"
      },
      "edited_at": {
        "type": "date"
      }
    }
  }
}'

echo ""

# ============================================================
# ÍNDICE: forum_reactions
# ============================================================
echo "Creando índice forum_reactions..."
curl -X PUT "$ES_HOST/forum_reactions" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "10s"
  },
  "mappings": {
    "properties": {
      "reaction_id": {
        "type": "keyword"
      },
      "post_id": {
        "type": "keyword"
      },
      "thread_id": {
        "type": "keyword"
      },
      "user_id": {
        "type": "keyword"
      },
      "reaction_type": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      }
    }
  }
}'

echo ""

# ÍNDICE: forum_reports
echo "Creando índice forum_reports..."
curl -X PUT "$ES_HOST/forum_reports" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "report_id": {
        "type": "keyword"
      },
      "post_id": {
        "type": "keyword"
      },
      "thread_id": {
        "type": "keyword"
      },
      "reporter": {
        "properties": {
          "user_id": {"type": "keyword"},
          "username": {"type": "keyword"}
        }
      },
      "reason": {
        "type": "keyword"
      },
      "description": {
        "type": "text"
      },
      "status": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      },
      "resolved_at": {
        "type": "date"
      },
      "resolved_by": {
        "type": "keyword"
      },
      "moderator_notes": {
        "type": "text"
      }
    }
  }
}'

echo ""
echo "✅ Todos los índices creados exitosamente"

# Verificar estado del cluster
echo ""
echo "Estado del cluster:"
curl -s "$ES_HOST/_cluster/health?pretty"

echo ""
echo "Índices creados:"
curl -s "$ES_HOST/_cat/indices?v"
