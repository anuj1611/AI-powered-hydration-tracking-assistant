from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory # You may need to install langchain-community
from dotenv import load_dotenv

load_dotenv()

class WaterIntakeAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
        # Dictionary to store history per user 
        self.memory = ChatMessageHistory() 
        
        # Define a prompt that explicitly handles history
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a hydration assistant. You remember the user's previous logs to provide progress-based feedback."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "I just consumed {intake_ml} ml of water. Provide status and suggest if I need more."),
        ])

    def analyze_intake(self, intake_ml: int):
        # 1 Create the chain
        chain = self.prompt_template | self.llm
        
        # 2 Invoke with current intake and existing history
        response = chain.invoke({
            "intake_ml": intake_ml,
            "chat_history": self.memory.messages
        })
        
        # 3 Save the interaction to memory
        self.memory.add_user_message(f"Logged {intake_ml} ml")
        self.memory.add_ai_message(response.content)
        
        return response.content
