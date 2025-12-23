import json
import uuid
from datetime import datetime
import chromadb
from langgraph.types import Command
from langgraph.graph import END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from .llm import llm_generica
from .schemas import InterestSchema

cliente = chromadb.PersistentClient(path="./chromadb")

def build_messages(estado, system_prompt):
    mensajes = [HumanMessage(content=system_prompt)]
    for m in estado["messages"]:
        mensajes.append(HumanMessage(content=m.content) if isinstance(m, HumanMessage) else AIMessage(content=m.content))
    return mensajes

def nodo_agente_recepcionista(estado: MessagesState) -> Command:
    r = llm_generica.invoke(build_messages(estado, "Eres un recepcionista cordial.","no entrges detalles de productos ni promociones o descuentos.", "manten la conversacion amable pero profesional")).content
    return Command(goto="agente_promotor", output=r)

def nodo_agente_promotor(estado: MessagesState) -> Command:
    schema = llm_generica.with_structured_output(InterestSchema)
    intereses = schema.invoke(build_messages(estado, "Extrae intereses del usuario.")).interest
    return Command(goto="agente_asesor", output=f"Detecté los siguientes intereses: {', '.join(intereses)}")

def nodo_agente_asesor(estado: MessagesState) -> Command:
    r = llm_generica.invoke(build_messages(estado, "Responde como asesor experto.")).content
    return Command(goto="agente_vendedor", output=r)

def nodo_agente_vendedor(estado: MessagesState) -> Command:
    pedido = {"id_venta": str(uuid.uuid4()), "fecha": datetime.now().isoformat(), "estado": "confirmado"}
    with open("./data/pedidos.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(pedido) + "\n")
    return Command(goto="agente_encuestador", output="Compra confirmada.")

def nodo_agente_encuestador(estado: MessagesState) -> Command:
    return Command(goto=END, output="Gracias por tu compra. ¿Deseas calificar la experiencia?")

def calificacion_experiencia(id_venta: int, puntuacion: int, recomendacion: int, comentario: str = "", canal: str = "chatbot"):
    if not 1 <= puntuacion <= 5:
        raise ValueError("La puntuación debe estar entre 1 y 5")
    experiencia = {"tipo": "Experiencia de compra", "id_venta": id_venta, "puntuacion": puntuacion, "recomendacion": recomendacion, "comentario": comentario, "canal": canal, "fecha": datetime.now().isoformat()}
    try:
        coleccion = cliente.get_collection("experiencia_compra")
    except Exception:
        coleccion = cliente.create_collection("experiencia_compra")
    coleccion.add(documents=[json.dumps(experiencia, ensure_ascii=False)], ids=[str(uuid.uuid4())], metadatas=[{"tipo": "experiencia_compra","id_venta": id_venta,"puntuacion": puntuacion}])