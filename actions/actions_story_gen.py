from pathlib import Path
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.api_llm.utils import query_llm
from actions.prompts.utils import load_prompt_template
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
        template = load_prompt_template(filename="continue_story.jinja2", templates_path=Path("actions/prompts"))
        rendered_template = template.render({
            "current_story": brief
        })
        response = query_llm(prompt=rendered_template)
        dispatcher.utter_message(text=response)
        return []
