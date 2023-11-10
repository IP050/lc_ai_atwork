from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel, Field
import os 


token = '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'

class Qa(BaseModel):
    question: str = Field(info="the question translated to dutch")
    answer: str = Field(info="the answer in a professional way")


def run_chain(query):
    llm = OpenAI(temperature=0, openai_api_key=token)
    
    parser = PydanticOutputParser(pydantic_object=Qa)
    prompt = PromptTemplate(
    template="You are {persona} Answer the user query in {language}. \n{format_instructions}\n{query}\n",
    input_variables=["query", "language", "persona"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return parser.parse(chain.run(query))
