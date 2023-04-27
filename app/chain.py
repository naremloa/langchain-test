from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain import ConversationChain
from langchain.llms.fake import FakeListLLM
from config import gen_llm_open_ai
from logger import logger
from langchain.callbacks import get_openai_callback
from langchain.document_loaders import WebBaseLoader
from pathlib import Path


if __name__ == "__main__":
    print("chain")


# tools = load_tools(["python_repl"])
# llm = FakeListLLM(
#     responses=[
#         "Action: Python REPL\nAction Input: print(2 + 2)",
#         "Final Answer: b",
#     ]
# )

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
# )


# agent.run("whats 2 + 2")

# loader = WebBaseLoader("https://www.digiknow.com.tw/knowledge/6425296595c7c")
# data = loader.load()
# logger.info(data.page_content)
