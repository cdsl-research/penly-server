from fastapi import FastAPI
from starlette.requests import Request
 


app = FastAPI()

@app.get('/')
def index(request: Request):
    return {'Hello': 'World'}

@app.get("/items")
def read_items(query_params: dict):
    keys = list(query_params.keys())
    return keys
