import json
import os
from typing import Text
import logging

import requests

from actions.utils import get_timestamp

logger = logging.getLogger(__name__)


def query_llm(prompt: Text):
    """
    Takes the prompt and uses appropriate llm service - huggingface/local ollama to get response.
    """
    llm_response = ""
    llm_error = False
    llm_service = os.environ["LLM_SERVICE"]
    if llm_service == "OLLAMA":
        model = os.environ["OLLAMA_MODEL"]
        url = os.environ["OLLAMA_URL"]
        if model is None or url is None:
            logger.error(f"OLLAMA environment variables not set: [OLLAMA_MODEL, OLLAMA_URL]")
            return ""
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            llm_response = response.json()['response']
        else:
            logger.error(f"Error querying OLLAMA; response: {response.json()}")
            llm_error = True
            llm_response = ""
    elif llm_service == "HUGGINGFACE":
        api_url = os.environ["HUGGINGFACE_API_URL"]
        api_key = os.environ["HUGGINGFACE_TOKEN"]
        if api_url is None or api_key is None:
            logger.error(f"HUGGINGFACE environment variables not set: [HUGGINGFACE_API_URL, HUGGINGFACE_TOKEN]")
            llm_error = True
            llm_response = ""
        response = requests.post(
            url=api_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
               "inputs": prompt,
            }
        )
        if response.status_code == 200:
            llm_response = response.json()[0].get("generated_text")
        else:
            logger.error(f"Error querying HUGGINGFACE; response: {response.json()}")
            llm_error = True
            llm_response = ""
    else:
        logger.error(f"No LLM_SERVICE environment variable set. Expected to be one of [OLLAMA, HUGGINGFACE]")
        llm_error = True
        llm_response = ""
    with open("actions/logs/query_llm_logs.txt", 'a', encoding="utf-8") as log_file:
        log_file.write(f"\n\n\n{'*' * 7} NEW REQUEST : {get_timestamp()} {'*' * 7}")
        log_file.write(f"\n{'*' * 7}** PROMPT  **{'*' * 7}\n")
        log_file.write(prompt)
        log_file.write(f"\n{'*' * 7}  RESPONSE   {'*' * 7}\n")
        if llm_error:
            log_file.write("LLM ERROR OCCURRED")
        else:
            log_file.write(llm_response)
        log_file.write(f"\n{'*' * 7}***  END  ***{'*' * 7}\n")
    return llm_response
