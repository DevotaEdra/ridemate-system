from ariadne import (
    load_schema_from_path, 
    make_executable_schema, 
    graphql_sync, 
    snake_case_fallback_resolvers, 
    ObjectType
)
from ariadne.asgi import GraphQL
from app.schema.resolvers import query, mutation # Pastikan import ini benar
from flask import Flask, request, jsonify
from app.database import Base, engine 
import app.models

Base.metadata.create_all(bind=engine)

# 1. Load Schema
type_defs = load_schema_from_path("app/schema/schema.graphql")

# 2. Buat Executable Schema
# PERHATIKAN BAGIAN INI: Tambahkan snake_case_fallback_resolvers ke dalam list
schema = make_executable_schema(
    type_defs, 
    [query, mutation, snake_case_fallback_resolvers]
)

# ... sisa code app Anda ...
app = GraphQL(schema, debug=True)
