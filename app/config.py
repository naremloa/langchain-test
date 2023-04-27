import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.llms import OpenAI
from llama_index import LLMPredictor, ServiceContext, MockLLMPredictor, MockEmbedding

load_dotenv()
open_api_key = os.environ.get("OP_KEY")

# ensure the cache directory
index_cache_web_dir = Path("./tmp/cache_web/")
index_cache_file_dir = Path("./tmp/cache_file/")
for cache_dir in [
    index_cache_web_dir,
    index_cache_file_dir,
]:
    if not cache_dir.is_dir():
        cache_dir.mkdir(parents=True, exist_ok=True)


def gen_llm_open_ai(
    max_tokens=256,
    temperature=0,
):
    llm = OpenAI(
        temperature=temperature,
        model_name="text-davinci-003",
        openai_api_key=open_api_key,
        # -1 returns as many tokens as possible
        max_tokens=max_tokens,
    )
    return llm


def gen_default_service_context(mock=False):
    max_tokens = -1
    llm_predictor = None
    embed_model = None
    llm = gen_llm_open_ai(max_tokens=max_tokens)
    if mock:
        llm_predictor = MockLLMPredictor(max_tokens=max_tokens, llm=llm)
        embed_model = MockEmbedding(embed_dim=1536)
    else:
        llm = gen_llm_open_ai(max_tokens=max_tokens)
        llm_predictor = LLMPredictor(llm=llm)
    return llm_predictor, embed_model


def gen_service_context(mock=True):
    # service context
    llm_predictor, embed_model = gen_default_service_context(mock=True)
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        embed_model=embed_model,
    )
    return service_context


# prompt
PROMPT_TEMPLATE = (
    "上下文信息如下所示： \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "我的问题是：{query_str}\n"
)
