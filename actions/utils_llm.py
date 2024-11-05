import json
import os
import random
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Tracker
import logging
from actions.api_llm.utils import query_llm


logger = logging.getLogger(__name__)


def select_response(
        domain: Dict[Text, Any],
        name: Text,
        channel: Text
) -> Optional[list]:
    """
    Retrieves response with name "name", filters by "channel" and
    selects random response among candidate responses.
    """
    responses = domain.get("responses", {}).get(name, [])
    channel_responses = [
        response for response in responses if response.get("channel") in [None, channel]
    ]
    if channel_responses is None:
        return None
    selected = random.choice(channel_responses)
    res_text = selected.get("text", None)
    rephrase = None
    prompt = None
    if res_text is not None:
        metadata = selected.get("metadata", None)
        if metadata is not None:
            rephrase = metadata.get("rephrase", None)
            prompt = metadata.get("rephrase_prompt", None)
    return [res_text, rephrase, prompt]


def fill_prompt(
        prompt: Text,
        suggested_response: Text,
        tracker: Tracker
) -> Text:
    """
    Description: Inserts the conversation history and current message in the space-holders in the given prompt.
    #TODO: insert conversation history
    """
    response = prompt
    response = response.replace("{{suggested_response}}", suggested_response)
    return response


def get_llm_rephrased(
        prompt: Text,
        fixed_response: Text,
        tracker: Tracker,
        text_completion=True
) -> Text:
    updated_prompt = fill_prompt(prompt=prompt, suggested_response=fixed_response, tracker=tracker)
    response = query_llm(updated_prompt)
    if text_completion is True:
        response = response.replace(updated_prompt,"")
        logger.debug(f"text completion response:\n{response}")
    else:
        logger.debug(f"rephrased response: {response}")
    return response


def get_llm_completion(
        prompt: Text,
) -> Text:
    response = query_llm(prompt)
    response = response.replace(prompt, "")
    return response


def llm_rephrase_response(
        domain: Dict[Text, Any],
        tracker: Tracker,
        name: Text,
) -> Optional[Text]:
    """
    Rephrases given response using LLM.
    """
    input_channel = tracker.get_latest_input_channel()
    fixed_response, rephrase_flag, prompt = select_response(
        domain=domain,
        name=name,
        channel=input_channel
    )
    if fixed_response is None:
        logger.error(f"Response {name} not found for rephrasing.")
        return None
    if rephrase_flag is True:
        response = get_llm_rephrased(prompt=prompt, fixed_response=fixed_response, tracker=tracker)
        return response
    return fixed_response


def query_llm_json(prompt: Text, max_retry: int = 10, current_retry: int = 0) -> dict:
    """
    The same as query_llm() but retries if response cannot be parsed into json.
    Args:
        current_retry:
        max_retry: Default 10.
        prompt (object):
    Returns parsed json as dict.
    #TODO put pydantic validation for json parsing.
    """
    if current_retry > max_retry:
        logger.error(f"max_retries exceeded for valid json type response. Returning empty dict.")
        return {}
    response = query_llm(prompt)
    try:
        as_dict = json.loads(response)
        return as_dict
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError) as e:
        logger.error(f"LLM response was not of valid json format. Error: {e}.\nRetrying({current_retry+1}/{max_retry}) again...")
        return query_llm_json(prompt=prompt, current_retry=current_retry+1)
    except Exception as e:
        logger.error(f"Unforeseen error occurred, could not change llm response to dict. Error: {e}. Aborting.")
        return {}
