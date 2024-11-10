from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.utils_llm import llm_rephrase_response
import logging


logger = logging.getLogger(__name__)


class ActionGreet(Action):
    """
    Description: Greets the user using LLM rephrasing.
    """
    def name(self) -> Text:
        return "action_greet"

    async def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        rephrased = llm_rephrase_response(
            tracker=tracker,
            domain=domain,
            name="utter_greet"
        )
        dispatcher.utter_message(text=rephrased)
        return []
