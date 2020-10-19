# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import random

import pymongo
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionRecommend(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client = pymongo.MongoClient("mongodb+srv://admin:hTQqJQUAtrOUGrgx@cluster0.8qnpj.mongodb.net")
        db = client["rasa_chatbot"]
        col = db["movies"]
        docs = list(col.find())
        movielist = []
        for data in docs:
            movielist.append(data["title"])

        randomsuggestion = random.randint(0, len(movielist) - 1)
        affectedMovie = docs[randomsuggestion]

        col.update_one({'_id': affectedMovie['_id']}, {'$set': {'suggestedCount': affectedMovie['suggestedCount'] + 1}},
                       upsert=False)
        #print(affectedMovie)

        dispatcher.utter_message(text="You can watch " + movielist[randomsuggestion])

        return []
