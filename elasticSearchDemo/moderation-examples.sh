#!/bin/bash

# Queries de moderación y anti-abuso

ES_HOST="http://localhost:9200"

echo "EJEMPLOS DE MODERACIÓN - ANTI-ABUSO"
echo ""

# 1. REPORTES PENDIENTES
echo "1️⃣  Reportes pendientes de moderación"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_reports/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"term": {"status": "pending"}}
      ],
      "filter": [
        {"range": {"created_at": {"gte": "now-7d"}}}
      ]
    }
  },
  "sort": [
    {"created_at": {"order": "desc"}}
  ],
  "_source": ["report_id", "post_id", "reason", "reporter.username", "created_at"],
  "size": 20
}' | jq '.hits.total.value as $total | "Total reportes pendientes: \($total)"'

echo ""
echo ""

# 2. POSTS MÁS REPORTADOS
echo "2️⃣  Posts más reportados (últimos 7 días)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_reports/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "query": {
    "range": {
      "created_at": {"gte": "now-7d"}
    }
  },
  "aggs": {
    "posts_mas_reportados": {
      "terms": {
        "field": "post_id",
        "size": 10,
        "order": {"_count": "desc"}
      },
      "aggs": {
        "razones": {
          "terms": {
            "field": "reason"
          }
        }
      }
    }
  }
}' | jq '.aggregations.posts_mas_reportados.buckets[] | {post_id: .key, reports: .doc_count, reasons: [.razones.buckets[].key]}'

echo ""
echo ""

# 3. OCULTAR POST REPORTADO
echo "3️⃣  Ejemplo: Ocultar post spam"
echo "-------------------------------------------"
curl -s -X POST "$ES_HOST/forum_posts/_update/post_spam_001?pretty" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "state": "hidden",
    "moderation": {
      "hidden_reason": "spam",
      "hidden_at": "2025-12-04T17:20:00Z",
      "hidden_by": "moderator_admin",
      "moderator_notes": "Promotional link to external casino site. User banned 7 days."
    }
  }
}' | jq '{result: .result, _id: ._id}'

echo ""
echo ""

# 4. POSTS OCULTOS (para revisión)
echo "4️⃣  Posts ocultos por moderación"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_posts/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {"state": "hidden"}
  },
  "sort": [
    {"moderation.hidden_at": {"order": "desc"}}
  ],
  "_source": ["post_id", "thread_title", "author.username", "moderation"],
  "size": 10
}' | jq '.hits.hits[] | {post_id: ._source.post_id, author: ._source.author.username, reason: ._source.moderation.hidden_reason, hidden_at: ._source.moderation.hidden_at}'

echo ""
echo ""

# 5. USUARIOS CON MÁS REPORTES RECIBIDOS
echo "5️⃣  Usuarios más reportados (últimos 30 días)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_reports/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "query": {
    "range": {
      "created_at": {"gte": "now-30d"}
    }
  },
  "aggs": {
    "posts_reportados": {
      "terms": {
        "field": "post_id",
        "size": 100
      }
    }
  }
}'

# Luego cruzar con forum_posts para obtener author.user_id
echo "Nota: En producción, esto se haría con un join en la aplicación"
echo ""
echo ""

# 6. RESOLVER REPORTE
echo "6️⃣  Ejemplo: Resolver reporte"
echo "-------------------------------------------"
curl -s -X POST "$ES_HOST/forum_reports/_update/report_001?pretty" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "status": "resolved",
    "resolved_at": "2025-12-04T17:30:00Z",
    "resolved_by": "moderator_admin",
    "moderator_notes": "Post hidden. User banned for 7 days."
  }
}' | jq '{result: .result, report_id: ._id}'

echo ""
echo ""

# 7. DISTRIBUCIÓN DE REPORTES POR RAZÓN
echo "7️⃣  Distribución de reportes por tipo"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_reports/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "reportes_por_razon": {
      "terms": {
        "field": "reason",
        "size": 10
      }
    }
  }
}' | jq '.aggregations.reportes_por_razon.buckets[] | {reason: .key, count: .doc_count}'

echo ""
echo ""

# 8. ACTIVIDAD DE MODERADORES
echo "8️⃣  Actividad de moderadores (últimos 7 días)"
echo "-------------------------------------------"
curl -s -X GET "$ES_HOST/forum_reports/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {"term": {"status": "resolved"}},
        {"range": {"resolved_at": {"gte": "now-7d"}}}
      ]
    }
  },
  "aggs": {
    "moderadores": {
      "terms": {
        "field": "resolved_by",
        "size": 10
      }
    }
  }
}' | jq '.aggregations.moderadores.buckets[] | {moderator: .key, reports_resolved: .doc_count}'

echo ""
echo ""

echo "Ejemplos de moderación completados"
