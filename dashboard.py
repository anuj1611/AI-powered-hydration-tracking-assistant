import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

if not st.session_state.tracker_started:
    st.title("💧 Welcome to AI Water Tracker")
    st.markdown("Track your daily hydration with the help of an AI assistant.")
    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()
else:
    st.title("💧 AI Water Tracker Dashboard")
    st.sidebar.header("Log Your Water Intake")

    user_id = st.sidebar.text_input("User ID", value="user_123")
    intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml > 0:
            log_intake(user_id, intake_ml)
            st.success(f"✅ Logged {intake_ml} ml")

            agent = WaterIntakeAgent(user_id=user_id)
            feedback = agent.analyze_intake(intake_ml)
            st.info(f"🤖 AI Feedback: {feedback}")
        else:
            st.warning("Please enter valid details.")

    st.markdown("---")
    st.header("Water Intake History")

    if user_id:
        history = get_intake_history(user_id)
        if history:
            # UPDATED: Matches the new database time format
            dates = [datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") for row in history]
            values = [row[0] for row in history]

            df = pd.DataFrame({
                "Time": dates,
                "Intake (ml)": values
            })

            # Sort by time to ensure chart flows correctly
            df = df.sort_values("Time")

            st.dataframe(df, use_container_width=True)
            # Line chart will now show the gap between logs based on minutes/hours
            st.line_chart(df, x="Time", y="Intake (ml)")
        else:
            st.warning("No logs found.")