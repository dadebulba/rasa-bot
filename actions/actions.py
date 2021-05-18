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
class ValidateCourseForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_course_form"
    
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
            #if "Laurea Triennale" in best_match[0] or "Laurea a Ciclo Unico" in best_match[0]:
            #    logger.debug("Entro in triennale ")
            #    dispatcher.utter_message(response="utter_topic/ammissioni_triennale")
            #else:
            #    dispatcher.utter_message(response="utter_topic/ammissioni_magistrale")
            #    logger.debug("Entro in magistrale ")
            return {"course": best_match[0]}
        else:
            dispatcher.utter_message(response="utter_wrong_course_type")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"course": None}

class ValidateStudiesForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_studies_form"
    
    def validate_studies(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        logger.debug("Course type action")
        course = tracker.get_slot("course")
        best_match = None
        if course == db.course_types[0]:
            best_match = difflib.get_close_matches(slot_value,db.lauree_triennali,1, cutoff=0.5)
        else:
            best_match = difflib.get_close_matches(slot_value,db.lauree_magistrali + db.lauree_ciclo_unico,1, cutoff=0.5)

        logger.debug(best_match)
        if len(best_match) > 0:
            logger.debug(best_match[0])
            # validation succeeded, set the value of the "cuisine" slot to value
            #if "Laurea Triennale" in best_match[0] or "Laurea a Ciclo Unico" in best_match[0]:
            #    logger.debug("Entro in triennale ")
            #    dispatcher.utter_message(response="utter_topic/ammissioni_triennale")
            #else:
            #    dispatcher.utter_message(response="utter_topic/ammissioni_magistrale")
            #    logger.debug("Entro in magistrale ")
            return {"studies": best_match[0]}
        else:
            dispatcher.utter_message(response="utter_wrong_course_type")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"studies": None}
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
class ActionAdmissions(Action):
    def name(self):
        return 'action_admissions'

    def run(self, dispatcher, tracker, domain):
        course = tracker.get_slot("course")
        if db.course_types[0] == course or db.course_types[1] == course:
            dispatcher.utter_message(response="utter_topic/ammissioni_triennale")
        else:
            dispatcher.utter_message(response="utter_topic/ammissioni_magistrale")
        return []
