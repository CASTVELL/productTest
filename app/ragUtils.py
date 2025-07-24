import os
from langchain import PromptTemplate, LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def build_retriever(docs_path: str, persist_dir: str = "faiss_index"):
    # Carga y divide documentos para RAG
    loader = TextLoader(docs_path, encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Embeddings y almacenamiento FAISS
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    if os.path.exists(persist_dir):
        vectorstore = FAISS.load_local(persist_dir, embeddings)
    else:
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(persist_dir)

    return vectorstore.as_retriever(search_kwargs={"k": 5})

# Prompt para extraer direcciones en JSON
extract_prompt = PromptTemplate(
    template="""
Extrae todas las direcciones postales del siguiente texto en español colombiano.
Devuelve la salida como JSON con campos: tipo_via, numero_via, numero_principal y numero_secundario.

Texto:
"""
)

# Prompt para generar homónimos de una dirección
homonimos_prompt = PromptTemplate(
    template="""
Dada esta dirección en JSON:
{address_json}

Genera al menos 5 variantes u homónimos realistas en español colombiano.
Devuélvelas como una lista JSON de cadenas.
"""
)

def extract_addresses(rag_retriever, text: str):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=rag_retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": extract_prompt}
    )
    result = qa.run(text)
    return result

def generate_homonimos(address_json: str):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    chain = LLMChain(llm=llm, prompt=homonimos_prompt)
    variants = chain.run(address_json=address_json)
    return variants

