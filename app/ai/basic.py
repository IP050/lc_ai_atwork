import os

from langchain import LLMMathChain, OpenAI

OPENAI_API_KEY = "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"

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = LLMMathChain(llm=llm, verbose=True)
