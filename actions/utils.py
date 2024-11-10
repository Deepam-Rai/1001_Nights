from datetime import datetime
import logging
from typing import List, Dict, Text, Any, Optional
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.slots import FloatSlot, BooleanSlot, TextSlot, ListSlot, AnySlot
from rasa_sdk import Tracker
from rasa.shared.core.events import UserUttered, BotUttered


logger = logging.getLogger(__name__)


def get_timestamp():
    return f"{datetime.fromtimestamp(datetime.timestamp(datetime.now())).isoformat()}"


def get_metadata(events: List[Dict[Text, Any]]) -> Dict[Text, Any]:
    """
    Extracts and returns metadata from the latest user message.
    :param events:
    :return:
    """
    for single_event in events[::-1]:
        if single_event.get("event") == "user":
            return single_event.get("metadata")
    return {}


def get_conversation_history(
        tracker: Tracker,
        human_prefix: str = "User",
        ai_prefix: str = "AI",
        max_turns: Optional[int] = 5,
) -> str:
    f"""
    Returns conversation between ai/bot and user as:
    Args:
        tracker: 
        human_prefix: the prefix to use for human utterances
        ai_prefix: the prefix to use for ai utterances
        max_turns: the maximum number of turns to include in the transcript
    Returns:
    human_prefix: some user message
    ai_prefix: the AI response
    human_prefix: another user message
    .
    .
    """

    def to_slot_object(name, value):
        """
        converts given key-value map to slot object. Tries best to guess correct slot type.
        :return:
        """
        map = {
            float: FloatSlot,
            bool: BooleanSlot,
            str: TextSlot,
            list: ListSlot,
        }
        slot = map.get(type(value), AnySlot)(name=name, mappings={}, initial_value=value, influence_conversation=False)
        return slot
    slots = [
        to_slot_object(name, value) for name, value in tracker.slots.items()
    ]
    d_tracker = DialogueStateTracker.from_dict(
        sender_id=tracker.sender_id,
        events_as_dict=tracker.events,
        slots=slots,
    )
    transcript = tracker_as_readable_transcript(
        d_tracker,
        human_prefix=human_prefix,
        ai_prefix=ai_prefix,
        max_turns=max_turns
    )
    return transcript


def tracker_as_readable_transcript(
    tracker: DialogueStateTracker,
    human_prefix: str = "User",
    ai_prefix: str = "AI",
    max_turns: Optional[int] = 20,
) -> str:
    """Creates a readable dialogue from a tracker.

    Args:
        tracker: the tracker to convert
        human_prefix: the prefix to use for human utterances
        ai_prefix: the prefix to use for AI utterances
        max_turns: the maximum number of turns to include in the transcript

    Example:
        ... tracker = Tracker(
        ...     sender_id="test",
        ...     slots=[],
        ...     events=[
        ...         UserUttered("hello"),
        ...         BotUttered("hi"),
        ...     ],
        ... )
        ... tracker_as_readable_transcript(tracker)
        human_prefix: hello
        ai_prefix: hi

    Returns:
    A string representing the transcript of the tracker
    """
    transcript = []

    def sanitize_message_for_prompt(text: Optional[str]) -> str:
        return text.replace("\n", " ") if text else ""
    for event in tracker.events:
        if isinstance(event, UserUttered):
            transcript.append(
                f"{human_prefix}: \"{sanitize_message_for_prompt(event.text)}\""
            )
        elif isinstance(event, BotUttered):
            transcript.append(f"{ai_prefix}: \"{sanitize_message_for_prompt(event.text)}\"")
    if max_turns:
        transcript = transcript[-max_turns:]
    transcript = "\n".join(transcript)
    return transcript
