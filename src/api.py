from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from src.logger import log_message, log_error

app = FastAPI(title="AI Powered Hydration Tracking API")

agent = WaterIntakeAgent()


class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.post("/log-intake")
async def log_water_intake(request: WaterIntakeRequest):
    try:
        # Store in database
        log_intake(request.user_id, request.intake_ml)

        # AI analysis
        analysis = agent.analyze_intake(request.intake_ml)

        # Log event
        log_message(
            f"User {request.user_id} logged {request.intake_ml} ml"
        )

        return {
            "message": "Water intake logged successfully",
            "analysis": analysis
        }

    except Exception as e:
        log_error(str(e))
        return {"error": "Something went wrong while processing intake"}


@app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    return {
        "user_id": user_id,
        "history": history
    }
