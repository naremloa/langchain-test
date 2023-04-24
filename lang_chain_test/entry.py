"""入口"""
import logging
import sys
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


documents = SimpleDirectoryReader("data").load_data()
index = GPTSimpleVectorIndex.from_documents(documents=documents)

index.save_to_disk("index.json")

# response = index.query("What did the author do growing up?")
# print(response)
