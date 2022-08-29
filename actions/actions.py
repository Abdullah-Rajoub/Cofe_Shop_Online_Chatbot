# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# #
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # listDrinks = []
#         # listDrinks.append(tracker.get_slot("drinks"))
#         # listBakery = []
#         # listBakery.append(tracker.get_slot("bakery"))
#         # listnumber = []
#         # listnumber.append(tracker.get_slot("drinks"))
#         # for x in listBakery:

#         dispatcher.utter_message(text="You want,"+)

#         return []
import json
from pathlib import Path
from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet

global nameDrink


# class ActionDrinksOrder(Action):

#     def name(self) -> Text:
#         return "action_drinks_order"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         nameDrink = ""
#         for blob in tracker.latest_message['entities']:
#             print(tracker.latest_message)
#             if blob['entity'] == 'drinks':
#                 nameDrink = blob['value']
#                 # dispatcher.utter_message(
#                 #     text="You have order: {}.".format(name))
#         return []

orders={"drinks":{"small":{},"medium":{},"large":{}},"bakery":{}}

#Has all items in menu and with prices 
menu={
    "drinks":{
        #small size price
        "small":{
            "black coffee":10,
            "latte":15,
            "iced latte":15,
            "iced coffee":14,
            "cappuccino":12
         }
         ,
         #medium size price
         "medium":{
            "black coffee":15,
            "latte":20,
            "iced latte":20,
            "iced coffee":19,
            "cappuccino":17
         }
         ,
         #large size price
         "large":{
            "black coffee":20,
            "latte":25,
            "iced latte":25,
            "iced coffee":24,
            "cappuccino":22
         }
    }
    ,
    "bakery":{
        #cookie  price
        "cookie": 10
         ,
         #croissant  price
         "croissant":15
         ,
         #begal  price
         "begal":20
         ,
         #donut  price
         "donut":5
    }

}

def order_add(category,item,amount,size):
    if amount==0:
        amount=1
    # drink case
    if category =="drinks":
        #check in the size lits
        if(size=="small"):
            if item in orders["drinks"]["small"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["small"][item]
                amount+=previous_amount
                orders["drinks"]["small"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["small"][item]=amount
        elif(size=="medium"):
            if item in orders["drinks"]["medium"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["medium"][item]
                amount+=previous_amount
                orders["drinks"]["medium"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["medium"][item]=amount        
        elif(size=="large"):
            if item in orders["drinks"]["large"].keys():
                # if it is already there grab it and add new amount to it 
                previous_amount=orders["drinks"]["large"][item]
                amount+=previous_amount
                orders["drinks"]["large"][item]=amount
            else:
                #First time ordered 
                orders["drinks"]["large"][item]=amount 

    ## for bakery items 
    if category =="bakery":
        #check if it is there 
        if item in orders["bakery"].keys():
             # if it is already there grab it and add new amount to it 
            previous_amount=orders["bakery"][item]
            amount+=previous_amount
            orders["bakery"][item]=amount
        else:
            #First time ordered 
            orders["bakery"][item]=amount


def calculate_bill():
    bill_list=[]
    cost=0
    for category in orders.keys():
        if category=="drinks":
            for size,items in orders["drinks"].items():
                for item,value in items.items():
                    #seeing item price in menu 
                    for category_menu in menu.keys():
                        if category_menu=="drinks":
                            for size_menu,items_menu in menu["drinks"].items():
                              if (size_menu==size):
                                for item_menu,value_menu in items_menu.items():
                                  if(item_menu==item):
                                    description=str(item)+" # "+str(value)+" price per item: "+str(value_menu)+" total with  "+str(((value*value_menu)+(value*value_menu*0.15)))
                                    #adding it to the main bill
                                    bill_list.append(description)
                                    #adding over all cost
                                    cost+=((value*value_menu))
                                
                                    
        else:
            for item,value in orders["bakery"].items():
              for item_menu,value_menu in menu["bakery"].items():
                              if(item_menu==item):
                                    description=str(item)+" # "+str(value)+" price per item: "+str(value_menu)+" total with  "+str(((value*value_menu)+(value*value_menu*0.15)))
                                    #adding it to the main bill
                                    bill_list.append(description)
                                    #adding over all cost
                                    cost+=((value*value_menu))
    #return the bill to be
    cost=cost+(cost*0.15)
    bill="Thanks for buying\nYour have ordered the following\n"
    for record in  bill_list:
      bill+= record+"\n"

    
    bill+="***** Your total bill amount is (" +str(cost) +" SAR) *****"                          
    return bill
 
                                    

from word2number import w2n       

class ActionBakeryOrder(Action):

    def name(self) -> Text:
        return "action_bakery_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('bakery')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            order_add("bakery",item,number,0)
            
           
            dispatcher.utter_message(
                    text="You have order: {} of {}.".format(number,item))
            
            return [SlotSet("bakery",""),
            SlotSet("number","one")]

class ActionDrinksOrder(Action):

    def name(self) -> Text:
        return "action_drinks_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            item=tracker.get_slot('drinks')
            number_str=tracker.get_slot('number')
            number_str=str(number_str)
            number=w2n.word_to_num(number_str)
            size=tracker.get_slot('size')
            order_add("drinks",item,number,size)
            
           
            dispatcher.utter_message(
                    text="You have order: {} # {} of size {}.".format(item,number,size))
                          
            return [SlotSet("drinks",""),
            SlotSet("number","one"),
            SlotSet("size","") ]

class ActionCheckOut(Action):

    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            bill =calculate_bill()
            orders={"drinks":{"small":{},"medium":{},"large":{}},"bakery":{}}
            dispatcher.utter_message(
                    text="{}".format(bill))
            #SlotSet("bill",bill)
            return []


# class ActionActionSize(Action):

#     def name(self) -> Text:
#         return "action_size"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         for blob in tracker.latest_message['entities']:
#             print(tracker.latest_message)
#             if blob['entity'] == 'size':
#                 name = blob['value']
#                 dispatcher.utter_message(
#                     text="The size of your order is: {}: {}.".format(name, nameDrink))
#         return []


# class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):
#     def __init__(self):
#         knowledge_base = InMemoryKnowledgeBase("data/pokemondb.json")
#         super().__init__(knowledge_base)
