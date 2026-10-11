import os
from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types

from app.prompt import ROOT_AGENT_INSTRUCTION
from tools.document_operation_tools.document_processing import analyze_document_next_chunk


# Free-tier models often return 503 (high demand) / 429 (rate limit); retry with backoff.
RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5, initial_delay=2, max_delay=30, http_status_codes=[429, 500, 503, 504]
)

root_agent = LlmAgent(
    name = "doc_analysis_agent",
    description = "Agent that analyzes documents in chunks and answers user questions.",
    model = Gemini(model=os.getenv("MODEL_NAME_AGENT"), retry_options=RETRY_OPTIONS),
    instruction = ROOT_AGENT_INSTRUCTION,
    tools = [analyze_document_next_chunk]
)


app = root_agent
