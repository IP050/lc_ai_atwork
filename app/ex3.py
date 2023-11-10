from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

OPENAI_API_KEY = "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"
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "The following is a friendly conversation between a human and an AI. The AI is an expert on a new tool that is being made. This tool will ." 
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
if __name__ == "__main__":
    print(conversation.run(input="Hi there!"))
    
    
