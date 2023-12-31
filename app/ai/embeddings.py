from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.fake import FakeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


OPENAI_API_KEY = "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"
loader = TextLoader("Readme.md")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = FakeEmbeddings(size=1536)
docsearch = Chroma.from_documents(texts, embeddings)

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY),
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
)


if __name__ == "__main__":
    # Run the chain only specifying the input variable.
    print(chain.run(question="colorful socks", chat_history=[]))