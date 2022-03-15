from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional

class attributes(BaseModel):
    urlId : str
    inputLink : HttpUrl



app = FastAPI()

@app.post("/")
def create_item(a: attributes):
    return {'message':{'attributes':{'urlId':a.urlId,'inputLink':a.inputLink}}}