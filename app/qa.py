from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from config import gen_llm_open_ai, open_api_key


def entry():
    loader = TextLoader("./web/742afed192a0391065163340276dd243/file.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
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

    query = "節能減碳的相關補助案"

    # result = vectordb.similarity_search(query, k=4)

    qa = RetrievalQA.from_chain_type(
        llm=gen_llm_open_ai(max_tokens=-1),
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    )

    result = qa.run(query)

    print("result", result)


if __name__ == "__main__":
    entry()
