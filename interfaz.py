import streamlit as st
import json
import uuid
import chromadb
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from multiagent.graph_builder import graph_builder

cliente = chromadb.PersistentClient(path="./chromadb")

st.title("🤖 Multi agente comercial MAC")

if st.button("Guardar catálogo"):
    try:
        coleccion = cliente.get_collection("catalogo_productos")
    except Exception:
        coleccion = cliente.create_collection("catalogo_productos")

    with open("./data/inventario.json", "r", encoding="utf-8") as f:
        inventario = json.load(f)

    for producto in inventario["productos"]:
        coleccion.add(
            documents=[json.dumps(producto, ensure_ascii=False)],
            ids=[str(uuid.uuid4())],
            metadatas=[{"id_producto": producto["id"]}],
        )

thread_id = str(uuid.uuid4())

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    st.chat_message(mensaje["role"]).write(mensaje["content"])

if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    lc_messages = [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in st.session_state.mensajes
    ]

    response = graph_builder.invoke(
        {"messages": lc_messages},
        config={"configurable": {"thread_id": thread_id}},
    )

    respuesta = response["messages"][-1].content
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    st.chat_message("assistant").write(respuesta)
