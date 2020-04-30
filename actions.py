from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import json
import send_mail
email_data = []
reverse_list = []

config = {"user_key": "3caa89ec8f0cef4cd898ffbd7b3e853c"}
zomato = zomatopy.initialize_app(config)


class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_search_restaurants'

    def run(self, dispatcher, tracker, domain):

        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        price = tracker.get_slot('price')
        print(price)
        location_detail = zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat = d1["location_suggestions"][0]["latitude"]
        lon = d1["location_suggestions"][0]["longitude"]
        cuisines_dict = {'mexican': 5, 'chinese': 25, 'american': 30, 'italian': 55, 'north indian': 50,
                         'south indian': 85}
        results = zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 10)
        d = json.loads(results)


        def list_sort(list):
            list.sort(key=lambda x: x[3])
            return list

        def Reverse(lst):
            return [ele for ele in reversed(lst)]

        global email_data
        global reverse_list
        response = ""
        if d['results_found'] == 0:
            response = "no results"
        else:
            if price =='Lesser than Rs. 300':
                for i,restaurant in enumerate(d['restaurants']):
                    averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                    if averageCostFor2 <= 300:
                        name = restaurant['restaurant']['name']
                        address = restaurant['restaurant']['location']['address']
                        #averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                        userrating = restaurant['restaurant']['user_rating']['aggregate_rating']

                        temp_list = [name,address,averageCostFor2,userrating]
                        email_data.append(temp_list)

            elif price =='Rs. 300 to 700':
                for i,restaurant in enumerate(d['restaurants']):
                    averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                    if averageCostFor2 >= 300 and averageCostFor2 <= 700:
                        name = restaurant['restaurant']['name']
                        address = restaurant['restaurant']['location']['address']
                        #averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                        userrating = restaurant['restaurant']['user_rating']['aggregate_rating']

                        temp_list = [name,address,averageCostFor2,userrating]
                        email_data.append(temp_list)
            elif price =='More than 700':
                for i,restaurant in enumerate(d['restaurants']):
                    averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                    if averageCostFor2 >= 700:
                        name = restaurant['restaurant']['name']
                        address = restaurant['restaurant']['location']['address']
                        #averageCostFor2 = restaurant['restaurant']['average_cost_for_two']
                        userrating = restaurant['restaurant']['user_rating']['aggregate_rating']

                        temp_list = [name,address,averageCostFor2,userrating]
                        email_data.append(temp_list)


        sorted_value  = list_sort(email_data)
        print(sorted_value)
        reverse_list = Reverse(sorted_value)

        def Enquiry(lis1):
            if not lis1:
                return 1
            else:
                return 0


        if Enquiry(sorted_value)==0:
            for i,x in enumerate(reverse_list):
                response = "NAME : "+str(x[0])+" ADDRESS : "+str(x[1])+" USER RATING : "+str(x[3])
                dispatcher.utter_message(response)
                if i ==5:
                    break
        else:
            dispatcher.utter_message("Sorry no result found ")


        return []


class SendMail(Action):
    def name(self):
        return 'action_send__mail'

    def run(self, dispatcher, tracker, domain):
        recivermail = tracker.get_slot('email')

        print(recivermail)

        emaildata = ""
        for x in reverse_list:
            print('-----',x)
            emaildata += "Name : "+ x[0] + " Address : "+ x[1] + " Price for 2 : "+str(x[2])+" Ratings : "+(x[3])+'\n'+'\n'

        send_mail.send_mail_gmail(emaildata, recivermail,"Resturant List for searched Location")
        dispatcher.utter_message("Mail send Please check your inbox")
        set_blank(reverse_list)

        return [SlotSet('email', recivermail)]

def set_blank(reverse_list):
    reverse_list =[]

class VerifyLocation(Action):
    def name(self):
        return 'action_verify_location'

    TIER_1 = []
    TIER_2 = []

    def __init__(self):
        self.TIER_1 = ['ahmedabad', 'bangalore', 'chennai',
                       'delhi', 'hyderabad', 'kolkata', 'mumbai', 'pune']
        self.TIER_2 = ['agra', 'ajmer', 'aligarh', 'allahabad', 'amravati', 'amritsar', 'asansol', 'aurangabad',
                       'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner',
                       'bokaro steel city', 'chandigarh', 'coimbatore', 'cuttack', 'dehradun', 'dhanbad',
                       'durg-bhilai nagar', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur',
                       'gulbarga', 'guntur', 'gurgaon', 'guwahati', 'gwalior', 'hubli-dharwad', 'indore', 'jabalpur',
                       'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kannur',
                       'kanpur', 'kakinada', 'kochi',
                       'kottayam', 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'lucknow', 'ludhiana',
                       'madurai', 'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore',
                       'nagpur', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 'pondicherry', 'raipur',
                       'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur',
                       'srinagar', 'sultanpur', 'surat', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli',
                       'tirunelveli', 'tiruppur', 'ujjain', 'vijayapura', 'vadodara', 'varanasi', 'vasai-virar city',
                       'vijayawada', 'visakhapatnam', 'warangal']

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        print(loc)
        if not (self.verify_location(loc)):
            dispatcher.utter_message(
                "We do not operate in " + loc + " yet. Please try some other city.")
            print('inside no')
            return [SlotSet('location', None), SlotSet("location_ok", False)]
        else:
            dispatcher.utter_message(
                "Great we serve in " + loc + ".")
            return [SlotSet('location', loc), SlotSet("location_ok", True)]

    def verify_location(self, loc):
        return loc.lower() in self.TIER_1 or loc.lower() in self.TIER_2


