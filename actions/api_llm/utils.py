import os
from typing import Text
import logging
from actions.api_llm.huggingface import HuggingFace


logger = logging.getLogger(__name__)


def query_llm(prompt: Text):
    """
    Takes the prompt and uses appropriate llm service - huggingface/local ollama to get response.
    """
    llm_service = os.environ["LLM_SERVICE"]
    if llm_service == "LOCAL_OLLAMA":
        pass
    elif llm_service == "HUGGINGFACE":
        api_url = os.environ["HUGGINGFACE_API_URL"]
        api_key = os.environ["HUGGINGFACE_TOKEN"]
        if api_url is None or api_key is None:
            logger.error(f"HUGGINGFACE environment variables not set: [HUGGINGFACE_API_URL, HUGGINGFACE_TOKEN]")
            return ""
        llm_api = HuggingFace(api_url, api_key)
        response = llm_api.get_text_completion(prompt)
        return response
    else:
        logger.error(f"No LLM_SERVICE environment variable set. Expected to be one of [LOCAL_OLLAMA, HUGGINGFACE]")
        return ""
