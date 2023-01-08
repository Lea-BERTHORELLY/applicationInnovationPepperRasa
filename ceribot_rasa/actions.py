# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/



# This is a simple example for a custom action which utters "Hello World!"


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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


from meteofrance_api import MeteoFranceClient
from meteofrance_api.helpers import readeable_phenomenoms_dict

class ActionWeather(Action):
  def name(self) -> Text:
      return "action_weather"
  def run(self, dispatcher: CollectingDispatcher,
          tracker: Tracker,
          domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client = MeteoFranceClient()
        place = client.search_places(tracker.get_slot("ville"))
        ville = place[0]
        prevision = client.get_forecast_for_place(ville)
        temperature = float( prevision.current_forecast["T"]["value"])
        temperature = int(temperature)
        text = "Il fait actuellement %s degrés Celsius à %s" % (str(temperature), ville.name)
        dispatcher.utter_message(text)
        return []

import requests
import json
class ActionMovies(Action):
    def name(self) -> Text :
        return "action_movies"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        titles=[]
        query = 'https://api.themoviedb.org/3/movie/popular?api_key=a535455b5f0157b1298fce29df4a5b3c&language=fr-FR&page=1'
        response =  requests.get(query)
        if response.status_code==200:
            array = response.json()
            for i in range(0,3):
                titles.append(array["results"][i]["title"])
            text = json.dumps(titles)
            dispatcher.utter_message("Les films à voir en ce moment sont : "+titles[0]+", "+titles[1]+" et "+titles[2]+".")
            return []
        else:
            dispatcher.utter_message("Je suis désolé mais je ne peux pas récupérer les films")
            return []

import datetime
from datetime import datetime,date,timedelta

class Edt(Action):
    def name(self) -> Text :
        return "action_schedule"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date = datetime.now()
        annee=date.year
        mois = date.month
        if(mois <10):
            mois = "0"+str(mois)
        jour=date.day
        if(jour <10):
            jour = "0"+str(jour)
        date_aujourdhui=str(annee)+"-"+str(mois)+"-"+str(jour)
        cours=[]
        liste_cours=[]

        specialite=tracker.get_slot("spe")
        groupe=tracker.get_slot("group")
        if (specialite=="ia"):
            query = 'https://api-edt.rasfi.me/ia/'+groupe[0:3]+'/'+date_aujourdhui
        else :
            query = 'https://api-edt.rasfi.me/'+specialite+'M2/'+groupe[0:3]+'/'+date_aujourdhui
        response =  requests.get(query)
        if response.status_code==200:
            array = response.json()
            for i in range(0,len(array)):
                datee = array[i]["start"].split("T")
                cours = array[i]["title"].replace("\n","*").replace("Matière : ","").split("*")
                
                debut_cours=datee[1].replace("+00:00","")
                debut_cours = datetime.strptime(debut_cours, '%H:%M:%S').time()
                
                if ((((debut_cours.hour+1)==date.hour) and ((debut_cours.minute)>=date.minute)) or ((debut_cours.hour+1)>date.hour)):
                    # print("Le cours va commencer à : "+ (str(debut_cours.hour+1)) + "h"+(str(debut_cours.minute))+", il est : "+ str(date.hour )+ "h" +(str(date.minute)))
                    liste_cours.append(cours[0])
            if (len(liste_cours)==0):
                text= {"text":"Vous n'avez pas d'autre cours aujourd'hui", "url": query}
            else:
                text={"text": liste_cours[0], "url": query}
            dispatcher.utter_message(json_message = text)
            return []
        else:
            dispatcher.utter_message({"text":"Je suis désolé mais je ne peux pas récupérer votre emploi du temps", "url": query})
            return []
