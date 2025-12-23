from langchain_community.chat_models import ChatOllama

llm_generica = ChatOllama(
    model="llama3",
    model_kwargs={"temperature": 0.7}
)