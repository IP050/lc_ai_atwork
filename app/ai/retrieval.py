from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.document_loaders import TextLoader
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os 


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
template = """Answer the question based only on the following context:

{context}

Question: {question}
"""

class Qa(BaseModel):
    question: str = Field(info="the question translated to dutch")
    answer: str = Field(info="the answer in a professional way")

parser = PydanticOutputParser(pydantic_object=Qa)
promptv2 = ChatPromptTemplate(
    template=template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(openai_api_key = OPENAI_API_KEY)

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def create_retriever(file_path: str) -> Chroma:
    chroma = Chroma()
    collections = chroma.get(include = ["metadatas"])
    print(collections)
    documents = open(file_path, "r", encoding="utf8").read() 
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = chroma.from_texts(texts, embeddings, collection_name="testing")
    print(db.get())
    return db.as_retriever()

def chainer(question, retriev):
    
    chain = (
        {"context": retriev | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(question)

