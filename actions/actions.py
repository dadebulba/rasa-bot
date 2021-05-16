from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.interfaces import Action
import difflib
import logging
import actions.db as db
logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')
logger.debug("starting actions")

class ValidateRestaurantForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_restaurant_form"

    @staticmethod
    def cuisine_db() -> List[Text]:
        """Database of supported cuisines."""

        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": value}
        else:
            dispatcher.utter_message(response="utter_wrong_cuisine")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cuisine": None}

    def validate_num_people(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return {"num_people": value}
        else:
            dispatcher.utter_message(response="utter_wrong_num_people")
            # validation failed, set slot to None
            return {"num_people": None}

    def validate_outdoor_seating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate outdoor_seating value."""

        if isinstance(value, str):
            if "out" in value:
                # convert "out..." to True
                return {"outdoor_seating": True}
            elif "in" in value:
                # convert "in..." to False
                return {"outdoor_seating": False}
            else:
                dispatcher.utter_message(response="utter_wrong_outdoor_seating")
                # validation failed, set slot to None
                return {"outdoor_seating": None}

        else:
            # affirm/deny was picked up as True/False by the from_intent mapping
            return {"outdoor_seating": value}

class ValidateCourseForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_course_form"
    
    @staticmethod
    def course_db() -> List[Text]:
        """Database of supported cuisines."""

        return ["Laurea Triennale", "Laurea a Ciclo Unico", "Laurea Magistrale"]

    def validate_course(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        logger.debug("Course type action")
        best_match = difflib.get_close_matches(slot_value,db.course_types,1, cutoff=0.5)
        logger.debug(best_match)
        if len(best_match) > 0:
            logger.debug(best_match[0])
            # validation succeeded, set the value of the "cuisine" slot to value
            if "Laurea Triennale" in best_match[0] or "Laurea a Ciclo Unico" in best_match[0]:
                logger.debug("Entro in triennale ")
                dispatcher.utter_message(response="utter_topic/ammissioni_triennale")
            else:
                dispatcher.utter_message(response="utter_topic/ammissioni_magistrale")
                logger.debug("Entro in magistrale ")
            return {"course": best_match[0]}
        else:
            dispatcher.utter_message(response="utter_wrong_course_type")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"course": None}

class ActionStudyPlan(Action):
    def name(self):
        return 'action_study_plan'

    def run(self, dispatcher, tracker, domain):
        course = tracker.get_slot("course")
        studies = tracker.get_slot("studies")
        if "Laurea Triennale" == course:
            for el in db.study_plan_triennali:
                if studies in el[0]: 
                    dispatcher.utter_message("Prova a vedere se qui ci sono le informazioni che stai cercando: " + el[1])
        else:
            for el in db.study_plan_magistrali:
                if studies in el[0]: 
                    dispatcher.utter_message("Prova a vedere se qui ci sono le informazioni che stai cercando: " + el[1])
        return []