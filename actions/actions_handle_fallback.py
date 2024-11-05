from pathlib import Path
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.constants import TILL_NOW
from actions.prompts.utils import load_prompt_template
import logging
from actions.utils_llm import query_llm_json


logger = logging.getLogger(__name__)


class ActionHandleFallback(Action):

    def name(self) -> Text:
        return "action_handle_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        till_now = tracker.get_slot(TILL_NOW) or ""
        brief = till_now.split(".")[-2:]
        brief = ". ".join(brief)
        latest_message = tracker.latest_message.get("text")
        template = load_prompt_template(filename="fallback.jinja2", templates_path=Path("actions/prompts"))
        rendered_template = template.render({
            "current_story": brief,
            "latest_message": latest_message
        })
        response = query_llm_json(prompt=rendered_template)
        if response.get("alter_story", False):
            dispatcher.utter_message(response="utter_story_alter")
        elif response.get("add_story", False):
            dispatcher.utter_message(response="utter_story_add")
        else:
            dispatcher.utter_message(text="non-story request")
        dispatcher.utter_message(text=response.get("response", "oops something went wrong!"))
        return []

