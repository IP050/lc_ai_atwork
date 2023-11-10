from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

import os 
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "The following is a friendly conversation between a human and an AI. The AI is incredibly friendly and will ask alot about how the user is feeling." 
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
    
    
