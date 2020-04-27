## complete path
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
    - slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_price_range
* restaurant_search{"price":"Lesser than Rs. 300"}
    - slot{"price": "Lesser than Rs. 300"}
    - action_search_restaurants
    - slot{"location": "delhi"}
    - slot{"cuisine": "chinese"}
    - utter_ask_email
* restaurant_search{"email":"raajrajnish@gmail.com"}
    - slot{"email": "raajrajnish@gmail.com"}
    - action_send_user_mail
    - slot{"email": "raajrajnish@gmail.com"}
    - utter_goodbye
    - export


## interactive_story_1
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "Delhi"}
    - slot{"location": "Delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_price_range
* restaurant_search{"price": "Lesser than Rs. 300"}
    - slot{"price": "Lesser than Rs. 300"}
    - action_search_restaurants
    - utter_ask_email
* sendmail
    - action_send_user_mail
    - utter_goodbye
    - utter_goodbye
