# GraphStore schema — namespaces

## Overview

GraphStore uses PostgreSQL schemas to separate concerns:

- `temporal.*` — Temporal Entity Graph (entity resolution, facts, edges)
- `rag_policy.*` — RAG policy rules and chunk storage

This separation ensures clean boundaries between temporal and RAG data.

## Migration script

See `migrate_graphstore_namespaces.sql` for the schema migration.
