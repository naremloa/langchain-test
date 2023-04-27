from logger import logger
from config import index_cache_file_dir, open_api_key, PROMPT_TEMPLATE, gen_service_context
from llama_index import SimpleDirectoryReader, QuestionAnswerPrompt, GPTSimpleVectorIndex
from util import get_name_md5

mock = False


def get_prompt_template():
    return QuestionAnswerPrompt(PROMPT_TEMPLATE)


def get_documents_by_file(path: str):
    documents = SimpleDirectoryReader(path).load_data()
    return documents


def get_index_from_file_cache(name: str):
    file_cache = index_cache_file_dir / name
    if not file_cache.is_file():
        return None
    index = GPTSimpleVectorIndex.load_from_disk(
        file_cache,
        service_context=gen_service_context(mock=mock),
    )
    logger.info(f"Get index from file cache: {file_cache}")
    return index


def entry(message: str, path: str):
    index_name = get_name_md5(path)
    index = get_index_from_file_cache(index_name)
    if index is None:
        documents = get_documents_by_file(path)
        index = GPTSimpleVectorIndex.from_documents(
            documents=documents,
            service_context=gen_service_context(mock=mock),
        )
        index.save_to_disk(index_cache_file_dir / index_name)
    prompt = get_prompt_template()
    answer = index.query(message, text_qa_template=prompt)
    logger.info(f"Answer: {answer}")
    return answer


if __name__ == "__main__":
    entry(
        message="幫我總結這篇文章的內容",
        path="./documents",
    )
