import streamlit as st
from langchain.llms.base import LLM
from groq import Groq
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import pandas as pd
from pydantic import BaseModel, Field, PrivateAttr
import re

# Crear un modelo de lenguaje Groq
class GroqLLM(LLM):
    api_key: str = Field(description="La API key de Groq")

    # Usar PrivateAttr para evitar que pydantic valide el atributo groq_model
    _groq_model: Groq = PrivateAttr()

    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)  # Inicializar los campos de pydantic
        self._groq_model = Groq(api_key=api_key)  # Inicializar el cliente de GroqAI

    def _call(self, prompt: str, **kwargs):
        # Hacer una solicitud a la API de GroqAI
        response = self._groq_model.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Eres un asistente útil que responde en español."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self):
        return "groq"

# Crear un modelo de lenguaje LangChain
api_key = "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"  # Reemplaza con tu API key de Groq
llm = GroqLLM(api_key=api_key)

# Cargar la base de conocimientos
knowledge_base_path = "knowledge_base/"
files = os.listdir(knowledge_base_path)
knowledge_base = []
for file in files:
    with open(os.path.join(knowledge_base_path, file), "r", encoding="utf-8") as f:
        knowledge_base.append(f.read())

# Crear embeddings de la base de conocimientos
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
text_embeddings = list(zip(knowledge_base, [embeddings.embed_query(doc) for doc in knowledge_base]))

# Indexar los embeddings utilizando FAISS
faiss_index = FAISS.from_embeddings(text_embeddings, embeddings)

# Crear un retriever
retriever = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=faiss_index.as_retriever(search_kwargs={"k": 3}),  # Recuperar los 3 documentos más relevantes
    verbose=True,
)

# Cargar el archivo de saldos
saldos_path = "saldo.csv"
saldos_df = pd.read_csv(saldos_path)

# Función para extraer el nombre del cliente de la pregunta
def extraer_nombre_cliente(pregunta):
    # Usar una expresión regular para extraer el nombre después de "saldo" o "balance"
    match = re.search(r"(saldo|balance)\s+(de\s+)?([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)", pregunta, re.IGNORECASE)
    if match:
        return match.group(3).strip()  # Extraer el nombre
    return ""

# Función para buscar el saldo de un cliente
def buscar_saldo_cliente(nombre_cliente):
    # Buscar el saldo en el DataFrame
    cliente = saldos_df[saldos_df["Nombre"].str.contains(nombre_cliente, case=False, na=False)]
    if not cliente.empty:
        return cliente.iloc[0]["Balance"]
    return None

# Crear un agente de atención al cliente
def agente_atencion_al_cliente(pregunta):
    # Verificar si la pregunta está relacionada con saldos
    if "saldo" in pregunta.lower() or "balance" in pregunta.lower():
        # Extraer el nombre del cliente de la pregunta
        nombre_cliente = extraer_nombre_cliente(pregunta)
        
        if nombre_cliente:
            # Buscar el saldo del cliente en el DataFrame
            saldo_cliente = buscar_saldo_cliente(nombre_cliente)
            
            if saldo_cliente is not None:
                return f"El saldo de {nombre_cliente} es: ${saldo_cliente:.2f}."
            else:
                return f"No se encontró información del cliente {nombre_cliente}."
        else:
            return "Por favor, proporciona el nombre del cliente para consultar su saldo."
    else:
        # Obtener la respuesta basada en la base de conocimientos
        respuesta = retriever.run(pregunta)
        return respuesta

# Configurar el frontend con Streamlit
st.title("Agente de Atención al Cliente")
st.write("¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")

# Campo de entrada para la pregunta del usuario
pregunta = st.text_input("Escribe tu pregunta aquí:")

# Botón para enviar la pregunta
if st.button("Enviar"):
    if pregunta:
        # Obtener la respuesta del agente
        respuesta = agente_atencion_al_cliente(pregunta)
        # Mostrar la respuesta
        st.write("**Respuesta:**")
        st.write(respuesta)
    else:
        st.warning("Por favor, escribe una pregunta.")