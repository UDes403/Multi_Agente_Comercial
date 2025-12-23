from fastapi import APIRouter
from pydantic import BaseModel
from multiagent.graph_builder import graph_builder
from langchain_core.messages import HumanMessage
from multiagent.nodes import calificacion_experiencia

router = APIRouter()

class MensajeUsuario(BaseModel):
    contenido: str

class Calificacion(BaseModel):
    id_venta: str
    puntuacion: int
    recomendacion: int
    comentario: str = ""

@router.post("/chat")
def chat(mensaje: MensajeUsuario):
    lc_messages = [HumanMessage(content=mensaje.contenido)]
    response = graph_builder.invoke({"messages": lc_messages})
    respuesta = response["messages"][-1].content
    return {"respuesta": respuesta}

@router.post("/feedback")
def feedback(data: Calificacion):
    calificacion_experiencia(
        id_venta=int(data.id_venta),
        puntuacion=data.puntuacion,
        recomendacion=data.recomendacion,
        comentario=data.comentario
    )
    return {"status": "ok", "mensaje": "Feedback registrado"}
