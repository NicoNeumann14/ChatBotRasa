# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
 
from typing import Any, Text, Dict, List
import random
 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
 
# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence
 
class ActionPlayRPS(Action):
   
    def name(self) -> Text:
        return "action_play_rps"
 
    def computer_choice(self):
        generatednum = random.randint(1,3)
        if generatednum == 1:
            computerchoice = "stein"
        elif generatednum == 2:
            computerchoice = "papier"
        elif generatednum == 3:
            computerchoice = "schere"
       
        return(computerchoice)
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play rock paper scissors
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"Deine auswahl war {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"Ich habe {comp_choice} ausgesucht")
 
        if user_choice == "stein" and comp_choice == "schere":
            dispatcher.utter_message(text="Glückwunsch, du hast Gewonnen!")
        elif user_choice == "stein" and comp_choice == "papier":
            dispatcher.utter_message(text="Ich hab diese Runde Gewonnen.")
        elif user_choice == "papier" and comp_choice == "stein":
            dispatcher.utter_message(text="Glückwunsch, du hast Gewonnen!")
        elif user_choice == "papier" and comp_choice == "schere":
            dispatcher.utter_message(text="Ich hab diese Runde Gewonnen.")
        elif user_choice == "schere" and comp_choice == "papier":
            dispatcher.utter_message(text="Glückwunsch, du hast Gewonnen!")
        elif user_choice == "schere" and comp_choice == "stein":
            dispatcher.utter_message(text="Ich hab diese Runde Gewonnen.")
        else:
            dispatcher.utter_message(text="Das war ein Unentschieden")
 
        return []

#Timer, send some response after spezific time
import time
class ActionTimerAsk(Action):

    def name(self) -> Text:
        return "action_timer_ask"

    def countdown(self,t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            t -= 1
        return []

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Starte den Counter..")
        d = self.countdown(10)
        dispatcher.utter_message(text="Eyyyyy die 60 sekunde sind vorbei, wach werden!!!!!!!")
 
        return []

#API-Call -> Http-Post to Bezeeptor
import requests
class CallRasaCore(Action):

    def name(self) -> Text:
        return "action_httpPost_Beceeptor"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = 'https://lm2022.free.beeceptor.com/RasaPost'
        myobj = {"sender":"Nico", "text":"UserEingabe"}

        x = requests.post(url, json = myobj)

        dispatcher.utter_message(text=x.text)

        
        return []

import psycopg2
from psycopg2 import Error
class CallRasaCore(Action):

    def name(self) -> Text:
        return "action_call_dbcount"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            conn = psycopg2.connect(database="rasa",
                            host="postgres",
                            user="postgres",
                            password="123456",
                            port="5432")

            cursor = conn.cursor()

            cursor.execute("SELECT version();")
            record = cursor.fetchall()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
        finally:
            if(conn):
                cursor.close()
                conn.close()
            
        dispatcher.utter_message(text="DB CALL = "+record)

        return []