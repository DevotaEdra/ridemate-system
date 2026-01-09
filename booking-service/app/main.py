from ariadne import (
    load_schema_from_path, 
    make_executable_schema, 
    graphql_sync, 
    snake_case_fallback_resolvers, 
    ObjectType
)
from ariadne.asgi import GraphQL
from app.schema.resolvers import query, mutation 
from flask import Flask, request, jsonify
from app.database import Base, engine 
import app.models

Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("app/schema/schema.graphql")

schema = make_executable_schema(
    type_defs, 
    [query, mutation, snake_case_fallback_resolvers]
)

app = GraphQL(schema, debug=True)
