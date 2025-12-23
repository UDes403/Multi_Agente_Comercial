from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.types import Command
from langchain_core.messages import SystemMessage

from app.llm import llm_generica
from multiagent.nodes.recepcionista import nodo_agente_recepcionista
from multiagent.nodes.promotor import nodo_agente_promotor
from multiagent.nodes.asesor import nodo_agente_asesor
from multiagent.nodes.vendedor import nodo_agente_vendedor
from multiagent.nodes.encuestador import nodo_agente_encuestador
from .schemas import Router
from .nodes import *


#Miembros del multiagente
miembros = [
    "agente-recepcionista", 
    "agente_promotor", 
    "agente_asesor",
    "agente_vendedor", 
    "agente_encuestador"
]

#
class Router(TypedDict):
    next: Literal[
        "agente_recepcionista",
        "agente_promotor",
        "agente_asesor",
        "agente_vendedor",
        "agente_encuestador",
        "FINISH"
    ]

PROMPT_SYSTEM = ("Actua como supervisor encargado de gestionar la conversacion entre los"
    f"siguientes agentes: {miembros}. dada la siguiente solicitud del usuario,"
    "responda con el agente para que actue a continuacion. cada agente realizara una"
    "tarea y responderá con sus resultados y estado."
    "Al finalizar,responda con FINISH."
)

#Nodo supervisor
def nodo_supervisor(estado: MessagesState) -> Command:
    response = llm_generica.with_structured_output(Router).invoke([{"role": "system", "content": PROMPT_SYSTEM}] + estado["messages"])

    goto = response["next"]
    return Command(goto=END if goto == "FINISH" else goto)

#Grafo
builder = StateGraph(MessagesState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", nodo_supervisor)
builder.add_node("agente_recepcionista", nodo_agente_recepcionista)
builder.add_node("agente_promotor", nodo_agente_promotor)
builder.add_node("agente_asesor", nodo_agente_asesor)
builder.add_node("agente_vendedor", nodo_agente_vendedor)
builder.add_node("agente_encuestador", nodo_agente_encuestador)
graph_builder = builder.compile()
