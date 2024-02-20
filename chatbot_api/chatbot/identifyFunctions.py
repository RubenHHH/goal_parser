import re
from .util import getModelOutput, construct_prompt


# prefix= """
#     Given the user input after </SYS>, identify the user's intents / user goals. If any of the intents in the following list are implied by the user, add this intent to your response list: 
#     ["parking_recommendation", "ticket_availability", "weather_checking", "event_booking"]. 
#     The user has been instructed to make a request based on the following description: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking advice, ticket_availability, weather check, event_booking].'
#     The number of intents identified by you can range from 0 to 4 and an intent should not be repeated.
# """

prefix_functionIdentification= """
    The user input you will get after </SYS> will be one or multiple of the intents stated in the below list.
    
    Intents:
    - 'parking recommerndation': Indicates the user wants to know where to park their car, they will ask for a location.
    - 'ticket_availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather_checking': Indicates the user wants to know about the current weather or temperature.
    - 'event_booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.
    
    The user has been instructed to make a request based on the following context: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking_recommendation, ticket_availability, weather_checking, event_booking].'
    
    Instructions:
    1. Analyze the user input to determine which intents are present.
    2. Consider the context to understand the underlying meaning of the user input.
    3. Output the identified intents in a list and no other explanation.


    The number of intents identified by you can range from 0 to 4 and an intent should not be repeated.

    Output Guidelines:
    Your response must strictly be one of the following format, based on the user's input. Do not include any additional explanations, greetings, or any text beyond what is specified here. The format can be like a python list, where each identified intent is an element seperated by commas, and all elements are placed between square brackets.

"""


def identifyFunctions(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"identifyFucntions with {(message, status, notepad)}")

    prompt = construct_prompt(notepad['user_requests'], prefix_functionIdentification)
    output = getModelOutput(prompt, logger)

    pattern = r'\[(.*?)\]'
    functions = re.findall(pattern, output)

    if len(functions) == 0:
        notepad['functions'] += output
    
    notepad['functions'] += functions[0]
    status = 'FUCNTIONS'
    

    return (notepad['functions'], status, notepad)
