from openai import OpenAI

from xact.config.gen import config

llm_client = OpenAI(
    base_url=config.XACT_LLM_BASE_URL,
    api_key=config.XACT_LLM_API_KEY,
)
