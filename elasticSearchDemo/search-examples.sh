#!/bin/bash

# Queries de ejemplo para demostrar funcionalidad

ES_HOST="http://localhost:9200"

echo "EJEMPLOS DE BÚSQUEDA - FOROS DUOLINGO"
echo ""

# 1. BÚSQUEDA FULL-TEXT
echo "1️⃣  Búsqueda full-text: 'subjuntivo gramática'"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_posts/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": {
        "multi_match": {
          "query": "subjuntivo gramática",
          "fields": ["content^2", "thread_title"],
          "type": "best_fields",
          "fuzziness": "AUTO"
        }
      },
      "filter": [
        {"term": {"state": "visible"}}
      ]
    }
  },
  "highlight": {
    "fields": {
      "content": {"fragment_size": 150}
    }
  },
  "_source": ["post_id", "thread_title", "content", "author.username", "created_at"],
  "size": 5
}' | jq '.hits.hits[] | {post_id: ._source.post_id, author: ._source.author.username, snippet: .highlight.content[0]}'

echo ""
echo ""

# 2. LISTADO DE HILOS POR SECCIÓN
echo "2️⃣  Hilos de la sección 'Gramática Española'"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_threads/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"term": {"section.section_id": "spanish_grammar"}},
        {"term": {"state": "visible"}}
      ]
    }
  },
  "sort": [
    {"pinned": {"order": "desc"}},
    {"last_activity_at": {"order": "desc"}}
  ],
  "_source": ["thread_id", "title", "author.username", "statistics", "created_at"],
  "size": 10
}' | jq '.hits.hits[] | {thread_id: ._source.thread_id, title: ._source.title, posts: ._source.statistics.post_count, views: ._source.statistics.view_count}'

echo ""
echo ""

# 3. POSTS DE UN HILO ESPECÍFICO
echo "3️⃣  Posts del hilo 'thread_001' (paginado)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_posts/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"term": {"thread_id": "thread_001"}},
        {"term": {"state": "visible"}}
      ]
    }
  },
  "sort": [
    {"position": {"order": "asc"}},
    {"created_at": {"order": "asc"}}
  ],
  "_source": ["post_id", "author.username", "content", "reactions.total", "created_at"],
  "size": 50,
  "from": 0
}' | jq '.hits.hits[] | {position: ._source.position, author: ._source.author.username, content: ._source.content[0:80] + "...", reactions: ._source.reactions.total}'

echo ""
echo ""

# 4. HILOS MÁS POPULARES (por reacciones)
echo "4️⃣  Top 5 hilos más populares"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_threads/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"state": "visible"}
  },
  "sort": [
    {"statistics.reaction_count": {"order": "desc"}}
  ],
  "_source": ["thread_id", "title", "statistics", "language"],
  "size": 5
}' | jq '.hits.hits[] | {title: ._source.title, reactions: ._source.statistics.reaction_count, posts: ._source.statistics.post_count, lang: ._source.language}'

echo ""
echo ""

# 5. BÚSQUEDA POR IDIOMA Y TAGS
echo "5️⃣  Hilos en español con tag 'grammar'"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_threads/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"term": {"language": "es"}},
        {"term": {"tags": "grammar"}},
        {"term": {"state": "visible"}}
      ]
    }
  },
  "_source": ["title", "tags", "author.username", "created_at"],
  "size": 10
}' | jq '.hits.hits[] | {title: ._source.title, tags: ._source.tags, author: ._source.author.username}'

echo ""
echo ""

# 6. POSTS CON MÁS REACCIONES "HELPFUL"
echo "6️⃣  Posts más útiles (ordenados por reactions.helpful)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_posts/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"state": "visible"}
  },
  "sort": [
    {"reactions.helpful": {"order": "desc"}}
  ],
  "_source": ["post_id", "thread_title", "author.username", "reactions.helpful", "content"],
  "size": 5
}' | jq '.hits.hits[] | {thread: ._source.thread_title, author: ._source.author.username, helpful: ._source.reactions.helpful, content: ._source.content[0:100] + "..."}'

echo ""
echo ""

# 7. AGREGACIONES: Threads por idioma
echo "7️⃣  Distribución de hilos por idioma"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_threads/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "threads_por_idioma": {
      "terms": {
        "field": "language",
        "size": 10
      }
    }
  }
}' | jq '.aggregations.threads_por_idioma.buckets[] | {language: .key, count: .doc_count}'

echo ""
echo ""

# 8. BÚSQUEDA CON AUTOCOMPLETADO
echo "8️⃣  Autocompletado: 'phrase' (búsqueda por título)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_threads/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": {
        "match_phrase_prefix": {
          "title": {
            "query": "common phrase",
            "max_expansions": 10
          }
        }
      },
      "filter": [
        {"term": {"state": "visible"}}
      ]
    }
  },
  "_source": ["title", "section.section_name"],
  "size": 5
}' | jq '.hits.hits[] | {title: ._source.title, section: ._source.section.section_name}'

echo ""
echo ""

echo "Ejemplos completados"
