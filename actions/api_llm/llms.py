import json
import requests
import time

import logging

logger = logging.getLogger(__name__)


class HuggingFace:
    """
    Huggingface inference API used for text completion/rephrasing.
    """
    def __init__(
            self,
            llm_api_url,
            api_key
    ):
        self.llm_url = llm_api_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def query(
            self,
            payload
    ):
        response = requests.post(
            url=self.llm_url,
            headers=self.headers,
            json=payload
        )
        return response.json()

    def get_text_completion(
            self,
            prompt
    ):
        logger.debug(f"LLM prompt given:\n{prompt}")
        payload = {
            "inputs": prompt,
        }
        response = self.query(payload=payload)
        logger.debug(f"LLM response: {response}")
        return response[0].get("generated_text")

    def get_creds(self, print=True):
        """ #TODO: """
        if print:
            print(f"LLM api url: {self.llm_url}")
            print(f"LLM api headers: {self.llm_headers}")
            return None
        return {
            "url": self.llm_url,
            "headers": self.headers
        }

# # Usage example
# import os
#
# api_url = os.getenv("LLM_API_URL"),
# api_key = os.getenv("LLM_API_KEY")
# print(f"LLM url: {api_url}   LLM api key: {api_key}")
#
# llm_api = HuggingFace(api_url, api_key)
# output = llm_api.query({"inputs": "Can you please let us know more details about your "})
# output = llm_api.get_text_completion("Can you please let us know more details about your ")
#
# print(output)
