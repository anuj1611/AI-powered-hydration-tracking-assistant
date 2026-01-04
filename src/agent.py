from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

class WaterIntakeAgent:
    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml: int):
        prompt = f"""
        You are a hydration assistant.
        The user has consumed {intake_ml} ml of water today.
        Provide hydration status and suggest if they need to drink more water.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content


if __name__ == "__main__":
    agent = WaterIntakeAgent()
    feedback = agent.analyze_intake(1500)
    print("Hydration Analysis:", feedback)
