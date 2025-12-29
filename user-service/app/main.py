from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path
from app.schema.resolvers import query, mutation
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

type_defs = load_schema_from_path("app/schema/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)

app = FastAPI()
app.mount("/graphql", GraphQL(schema, debug=True))
