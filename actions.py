from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import json
import send_mail

config={ "user_key":"3caa89ec8f0cef4cd898ffbd7b3e853c"}
zomato = zomatopy.initialize_app(config)

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'
		
	def run(self, dispatcher, tracker, domain):

		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price = tracker.get_slot('price')
		print(price)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
		d = json.loads(results)
		response=""
		if d['results_found'] == 0:
			response= "no results"
		else:
			for restaurant in d['restaurants']:
				response=response+ "Found "+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+"\n"
		
		dispatcher.utter_message("-----"+response)
		return [SlotSet('location',loc),SlotSet('cuisine',cuisine)]


class SendMail(Action):
	def name(self):
		return 'action_send_user_mail'

	def run(self, dispatcher, tracker, domain):
		recivermail = tracker.get_slot('email')
		print(recivermail)
		send_mail.send_mail_gmail("message 10 results",recivermail)
		dispatcher.utter_message("Mail send Please check your inbox")
		return [SlotSet('email',recivermail)]


