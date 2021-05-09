# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import actions.db as db
import difflib
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Action, Tracker

class ValidateCourseTypeForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_course_type_form"

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    
    def validate_course_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        best_match = difflib.get_close_matches(value,db.course_types,1, cutoff=0.5)
        if len(best_match) > 0:
            # validation succeeded, set the value of the "cuisine" slot to value
            if "Laurea Triennale" in best_match[0] or "Laurea a Ciclo Unico" in best_match[0]:
                dispatcher.utter_message(response="utter_topic/ammissioni_triennale")
            else:
                dispatcher.utter_message(response="utter_topic/ammissioni_magistrale")
            return {"course_type": best_match[0]}
        else:
            dispatcher.utter_message(response="utter_wrong_course_type")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"course_type": None}
class ValidateCourseChoiceForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_course_form"

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    
    def validate_course(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        course_type = tracker.get_slot("course_type")
        if course_type is "Laurea Triennale":
            best_match = difflib.get_close_matches(value,db.lauree_triennali,1, cutoff=0.5)
        elif course_type is "Laurea a Ciclo Unico":
            best_match = difflib.get_close_matches(value,db.lauree_ciclo_unico,1, cutoff=0.5)
        elif course_type is "Laurea Magistrale":
            best_match = difflib.get_close_matches(value,db.lauree_magistrali,1, cutoff=0.5)
        if len(best_match) > 0:
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"study_course": best_match[0]}
        else:
            dispatcher.utter_message(response="utter_wrong_study_course")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"study_course": None}
