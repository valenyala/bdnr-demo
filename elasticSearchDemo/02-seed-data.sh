#!/bin/bash

ES_HOST="http://localhost:9200"

echo "Insertando datos de prueba..."

# THREADS
echo "Insertando threads..."

# Thread 1: Gramática española
curl -X POST "$ES_HOST/forum_threads/_doc/thread_001" -H 'Content-Type: application/json' -d'
{
  "thread_id": "thread_001",
  "section": {
    "section_id": "spanish_grammar",
    "section_name": "Gramática Española"
  },
  "title": "¿Cuándo usar el subjuntivo?",
  "author": {
    "user_id": "user_123",
    "username": "maria_gomez",
    "display_name": "María Gómez"
  },
  "language": "es",
  "tags": ["grammar", "subjunctive", "question"],
  "state": "visible",
  "pinned": false,
  "locked": false,
  "statistics": {
    "post_count": 5,
    "view_count": 342,
    "reaction_count": 12,
    "last_post_at": "2025-12-04T16:30:00Z"
  },
  "created_at": "2025-12-03T10:00:00Z",
  "updated_at": "2025-12-04T16:30:00Z",
  "last_activity_at": "2025-12-04T16:30:00Z"
}'

# Thread 2: Vocabulario inglés
curl -X POST "$ES_HOST/forum_threads/_doc/thread_002" -H 'Content-Type: application/json' -d'
{
  "thread_id": "thread_002",
  "section": {
    "section_id": "english_vocabulary",
    "section_name": "English Vocabulary"
  },
  "title": "Common phrasal verbs for daily conversation",
  "author": {
    "user_id": "user_456",
    "username": "john_smith",
    "display_name": "John Smith"
  },
  "language": "en",
  "tags": ["vocabulary", "phrasal-verbs", "beginner"],
  "state": "visible",
  "pinned": true,
  "locked": false,
  "statistics": {
    "post_count": 15,
    "view_count": 1205,
    "reaction_count": 48,
    "last_post_at": "2025-12-04T15:00:00Z"
  },
  "created_at": "2025-12-01T08:00:00Z",
  "updated_at": "2025-12-04T15:00:00Z",
  "last_activity_at": "2025-12-04T15:00:00Z"
}'

# Thread 3: Pronunciación francesa
curl -X POST "$ES_HOST/forum_threads/_doc/thread_003" -H 'Content-Type: application/json' -d'
{
  "thread_id": "thread_003",
  "section": {
    "section_id": "french_pronunciation",
    "section_name": "Prononciation Française"
  },
  "title": "Comment prononcer les voyelles nasales?",
  "author": {
    "user_id": "user_789",
    "username": "pierre_dubois",
    "display_name": "Pierre Dubois"
  },
  "language": "fr",
  "tags": ["pronunciation", "phonetics", "intermediate"],
  "state": "visible",
  "pinned": false,
  "locked": false,
  "statistics": {
    "post_count": 8,
    "view_count": 567,
    "reaction_count": 23,
    "last_post_at": "2025-12-04T14:20:00Z"
  },
  "created_at": "2025-12-02T12:00:00Z",
  "updated_at": "2025-12-04T14:20:00Z",
  "last_activity_at": "2025-12-04T14:20:00Z"
}'

echo ""

# POSTS
echo "Insertando posts..."

# Posts para thread_001
curl -X POST "$ES_HOST/forum_posts/_doc/post_001" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_001",
  "thread_id": "thread_001",
  "thread_title": "¿Cuándo usar el subjuntivo?",
  "author": {
    "user_id": "user_123",
    "username": "maria_gomez",
    "display_name": "María Gómez"
  },
  "content": "Hola a todos, estoy estudiando español y tengo muchas dudas sobre cuándo debo usar el subjuntivo. ¿Alguien puede explicarme las reglas básicas? He leído que se usa después de expresiones de duda y emoción, pero me confundo mucho. Gracias!",
  "language": "es",
  "position": 1,
  "state": "visible",
  "reactions": {
    "like": 5,
    "helpful": 3,
    "love": 0,
    "total": 8
  },
  "created_at": "2025-12-03T10:00:00Z"
}'

curl -X POST "$ES_HOST/forum_posts/_doc/post_002" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_002",
  "thread_id": "thread_001",
  "thread_title": "¿Cuándo usar el subjuntivo?",
  "author": {
    "user_id": "user_555",
    "username": "carlos_teacher",
    "display_name": "Carlos Fernández"
  },
  "content": "¡Hola María! El subjuntivo se usa principalmente en tres casos: 1) Después de verbos de influencia (querer, necesitar, pedir), 2) Después de expresiones de duda (dudar, no creer), 3) Después de expresiones de emoción (me alegra, es triste). Por ejemplo: \"Espero que vengas mañana\" o \"Dudo que llueva hoy\". ¿Te ayuda esto?",
  "language": "es",
  "position": 2,
  "state": "visible",
  "reactions": {
    "like": 12,
    "helpful": 15,
    "love": 3,
    "total": 30
  },
  "created_at": "2025-12-03T11:30:00Z"
}'

curl -X POST "$ES_HOST/forum_posts/_doc/post_003" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_003",
  "thread_id": "thread_001",
  "thread_title": "¿Cuándo usar el subjuntivo?",
  "author": {
    "user_id": "user_123",
    "username": "maria_gomez",
    "display_name": "María Gómez"
  },
  "content": "¡Muchas gracias Carlos! Eso me aclara mucho. ¿Podrías darme algunos ejemplos más con verbos de influencia? Todavía me cuesta un poco.",
  "language": "es",
  "position": 3,
  "state": "visible",
  "reactions": {
    "like": 2,
    "helpful": 0,
    "love": 1,
    "total": 3
  },
  "created_at": "2025-12-03T12:15:00Z"
}'

# Posts para thread_002
curl -X POST "$ES_HOST/forum_posts/_doc/post_004" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_004",
  "thread_id": "thread_002",
  "thread_title": "Common phrasal verbs for daily conversation",
  "author": {
    "user_id": "user_456",
    "username": "john_smith",
    "display_name": "John Smith"
  },
  "content": "I wanted to share some common phrasal verbs that I use every day: wake up, get up, take off, put on, look after, find out. These are essential for basic conversations!",
  "language": "en",
  "position": 1,
  "state": "visible",
  "reactions": {
    "like": 25,
    "helpful": 18,
    "love": 5,
    "total": 48
  },
  "created_at": "2025-12-01T08:00:00Z"
}'

curl -X POST "$ES_HOST/forum_posts/_doc/post_005" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_005",
  "thread_id": "thread_002",
  "thread_title": "Common phrasal verbs for daily conversation",
  "author": {
    "user_id": "user_888",
    "username": "sarah_jones",
    "display_name": "Sarah Jones"
  },
  "content": "Great list! I would add: turn on/off (for lights), hang out (spend time with friends), give up (stop trying), and work out (exercise). These are super useful!",
  "language": "en",
  "position": 2,
  "state": "visible",
  "reactions": {
    "like": 15,
    "helpful": 12,
    "love": 2,
    "total": 29
  },
  "created_at": "2025-12-01T10:30:00Z"
}'

# Post con spam (oculto)
curl -X POST "$ES_HOST/forum_posts/_doc/post_spam_001" -H 'Content-Type: application/json' -d'
{
  "post_id": "post_spam_001",
  "thread_id": "thread_001",
  "thread_title": "¿Cuándo usar el subjuntivo?",
  "author": {
    "user_id": "user_spammer",
    "username": "casino_bot",
    "display_name": "Win Money"
  },
  "content": "Click here to win $10000! Best online casino! www.scam-casino-site.com",
  "language": "es",
  "position": 4,
  "state": "hidden",
  "reactions": {
    "like": 0,
    "helpful": 0,
    "love": 0,
    "total": 0
  },
  "moderation": {
    "hidden_reason": "spam",
    "hidden_at": "2025-12-04T16:00:00Z",
    "hidden_by": "moderator_admin",
    "moderator_notes": "Promotional link to external casino site"
  },
  "created_at": "2025-12-04T15:45:00Z"
}'

echo ""

# REACTIONS
echo "Insertando reacciones..."

curl -X POST "$ES_HOST/forum_reactions/_doc/reaction_001" -H 'Content-Type: application/json' -d'
{
  "reaction_id": "reaction_001",
  "post_id": "post_002",
  "thread_id": "thread_001",
  "user_id": "user_123",
  "reaction_type": "helpful",
  "created_at": "2025-12-03T11:35:00Z"
}'

curl -X POST "$ES_HOST/forum_reactions/_doc/reaction_002" -H 'Content-Type: application/json' -d'
{
  "reaction_id": "reaction_002",
  "post_id": "post_002",
  "thread_id": "thread_001",
  "user_id": "user_999",
  "reaction_type": "like",
  "created_at": "2025-12-03T12:00:00Z"
}'

echo ""

# REPORTS
echo "Insertando reportes..."

curl -X POST "$ES_HOST/forum_reports/_doc/report_001" -H 'Content-Type: application/json' -d'
{
  "report_id": "report_001",
  "post_id": "post_spam_001",
  "thread_id": "thread_001",
  "reporter": {
    "user_id": "user_123",
    "username": "maria_gomez"
  },
  "reason": "spam",
  "description": "This post contains promotional links to a casino website",
  "status": "resolved",
  "created_at": "2025-12-04T15:50:00Z",
  "resolved_at": "2025-12-04T16:00:00Z",
  "resolved_by": "moderator_admin",
  "moderator_notes": "Post hidden. User banned for 7 days."
}'

curl -X POST "$ES_HOST/forum_reports/_doc/report_002" -H 'Content-Type: application/json' -d'
{
  "report_id": "report_002",
  "post_id": "post_spam_001",
  "thread_id": "thread_001",
  "reporter": {
    "user_id": "user_555",
    "username": "carlos_teacher"
  },
  "reason": "spam",
  "description": "Obvious spam content",
  "status": "resolved",
  "created_at": "2025-12-04T15:52:00Z",
  "resolved_at": "2025-12-04T16:00:00Z",
  "resolved_by": "moderator_admin"
}'

echo ""
echo "✅ Datos de prueba insertados exitosamente"

# Refrescar índices para que los datos sean inmediatamente buscables
echo ""
echo "Refrescando índices..."
curl -X POST "$ES_HOST/_refresh"

echo ""
echo "Conteo de documentos por índice:"
curl -s "$ES_HOST/_cat/count/forum_*?v"
