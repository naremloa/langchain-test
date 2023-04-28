from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain import ConversationChain
from langchain.llms.fake import FakeListLLM
from langchain.text_splitter import CharacterTextSplitter
from config import gen_llm_open_ai, open_api_key
from logger import logger
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from pathlib import Path
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


def entry():
    loader = TextLoader("./web/742afed192a0391065163340276dd243/file.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=open_api_key,
    )
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="db",
    )
    vectordb.persist()
    query = "什麼是 CCUS"
    docs = vectordb.similarity_search(query)
    print("docs", docs)
    # qa = RetrievalQA.from_chain_type(
    #     llm=gen_llm_open_ai(max_tokens=-1),
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
    # )
    # query = "這篇文章的標題是什麼"
    # result = qa.run(query)

    # print("answer: ", result)


if __name__ == "__main__":
    entry()
