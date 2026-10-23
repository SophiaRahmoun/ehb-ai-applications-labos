
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from labo_1.lokaal import voorspel_met_lokaal_model
from labo_1.regels import voorspel_met_regel
from labo_1.taalmodel import voorspel_met_taalmodel

app = FastAPI()


@app.get("/regel")
def regel(tekst: str):
    return {"sentiment": voorspel_met_regel(tekst)} 

@app.get("/lokaal")
def lokaal(tekst: str):
    return {"sentiment": voorspel_met_lokaal_model(tekst)}

@app.get("/taalmodel")
def taalmodel(tekst: str):
    return {"sentiment": voorspel_met_taalmodel(tekst)}
