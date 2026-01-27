import os

LLM_API_KEY = os.getenv("LLM_API_KEY", "tu-api-key-aqui")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://routellm.abacus.ai/v1")
BANKROLL = int(os.getenv("BANKROLL", "1000"))
KELLY_FRACTION = float(os.getenv("KELLY_FRACTION", "0.25"))
