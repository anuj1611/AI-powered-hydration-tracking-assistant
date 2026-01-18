import json
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, messages_from_dict, messages_to_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

class WaterIntakeAgent:
    def __init__(self, user_id="default"):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
        self.db_path = "water_tracker.db"
        self.user_id = user_id
        
        # System instructions make the AI aware of its role and memory
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a hydration assistant. Use the chat history provided to give progress-aware feedback. If the user has already logged water today, acknowledge it."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "I just consumed {intake_ml} ml of water. Provide status and suggestions."),
        ])

    def _get_history(self, limit=10):
        """Fetches last N messages from SQLite and converts them to LangChain objects."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT message_json FROM message_store WHERE session_id = ? ORDER BY id DESC LIMIT ?", (self.user_id, limit))
        rows = cursor.fetchall()
        conn.close()
        # History is retrieved in reverse order due to DESC, so we flip it
        msg_dicts = [json.loads(row[0]) for row in reversed(rows)]
        return messages_from_dict(msg_dicts)

    def _save_message(self, message):
        """Serializes and saves a message to SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        msg_dict = messages_to_dict([message])[0]
        cursor.execute("INSERT INTO message_store (session_id, message_json) VALUES (?, ?)", 
                       (self.user_id, json.dumps(msg_dict)))
        conn.commit()
        conn.close()

    def analyze_intake(self, intake_ml: int):
        # 1. Load history
        history = self._get_history()
        
        # 2. Build and invoke the chain
        chain = self.prompt_template | self.llm
        response = chain.invoke({
            "intake_ml": intake_ml,
            "chat_history": history
        })
        
        # 3. Store the new interaction in memory
        self._save_message(HumanMessage(content=f"Logged {intake_ml}ml"))
        self._save_message(AIMessage(content=response.content))
        
        return response.content
