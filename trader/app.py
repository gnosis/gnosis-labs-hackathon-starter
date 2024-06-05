import streamlit as st
from dotenv import load_dotenv
from prediction_market_agent_tooling.markets.agent_market import SortBy
from prediction_market_agent_tooling.markets.markets import (
    MarketType,
    get_binary_markets,
)

from trader.prediction import predict

# Load the environment variables.
load_dotenv()

# Get some open markets from Omen.
markets = get_binary_markets(42, MarketType.OMEN, sort_by=SortBy.CLOSING_SOONEST)

# Either select a market or provide a custom question.
custom_question_input = st.checkbox("Provide a custom question", value=False)
question = (
    st.text_input("Question")
    if custom_question_input
    else st.selectbox("Select a question", [m.question for m in markets])
)
if not question:
    st.warning("Please enter a question.")
    st.stop()

# Get the prediction.
prediction = predict(question)

# Display the prediction.
if prediction is None:
    st.error("The agent failed to generate a prediction")
    st.stop()

st.write(
    f"Prediction for the question: {'Yes, it will happen.' if question else 'No, it will not.'}",
)
