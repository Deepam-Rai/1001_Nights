from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.utils_llm import get_llm_completion
from actions.constants import *
import logging


logger = logging.getLogger(__name__)


class ActionContinueStory(Action):

    def name(self) -> Text:
        return "action_continue_story"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        till_now = tracker.get_slot(TILL_NOW)
        brief = till_now.split(".")[-2:]
        brief = ". ".join(brief)
        generated = get_llm_completion(brief)
        logger.debug(f"Received generated:{generated}")
        if generated.startswith(brief):
            logger.debug(f"Before lstrip:{generated}")
            generated = generated[len(brief):]
        gen_brief = generated.split(".")[:2]
        logger.debug(f"After split:\n{gen_brief}")
        gen_brief = ". ".join(gen_brief)
        logger.debug(f'Gen brief:\n{gen_brief}')
        dispatcher.utter_message(text=gen_brief)
        return []
