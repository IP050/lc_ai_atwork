from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel, Field
import os 


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class Qa(BaseModel):
    question: str = Field(info="the question translated to dutch")
    answer: str = Field(info="the answer in a professional way")


def run_chain(query):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    
    parser = PydanticOutputParser(pydantic_object=Qa)
    prompt = PromptTemplate(
    template="You are {persona} Answer the user query in {language}. \n{format_instructions}\n{query}\n",
    input_variables=["query", "language", "persona"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return parser.parse(chain.run(query))
