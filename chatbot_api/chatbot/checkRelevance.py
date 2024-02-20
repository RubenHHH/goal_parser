from .util import construct_prompt, getModelOutput
from .identifyFunctions import identifyFunctions


prefix_relevanceCheckStart= """
    Given the user input, determine if the request aligns with one of the following specified intents:

    Intents:
    
    - 'parking_recommendation': Indicates the user wants to know where to park their vehicle, they will ask for a location.
    - 'ticket_availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather_checking': Indicates the user wants to know about the current weather or temperature.
    - 'event_booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.
    
    Context: This service is tailored for attendees of the Street Science days in L'Aquila. Users are encouraged to make requests related to parking, ticketing for events, weather information, or event_bookings only.

    Your task is to analyze the user's input and identify whether it falls within the specified intents. If the input does not align with these intents, or includes requests outside the specified categories, instruct the user to refine their query according to the available services.

    Output Guidelines:
    Your response must strictly be one of the following, based on the user's input. Do not include any additional explanations, greetings, or any text beyond what is specified here.

    - If the user's request fall within the specified intents, respond with 'YES'.
    - If the requests are outside the specified intents, respond with: "What can I help you with? Your request should be one or multiple intents falling under the four listed above."
    - Do NOT say something like 'Based on the user's input, my response would be:'

    Ensure that your output matches one of these two options, word for word.

    Example User Inputs and Expected Responses:
    -> User: "How old am I?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Can I pet my dog?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I want to visit Rome". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I want to buy a car". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Where is my sandwich?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I feel lonely". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Where is the concert happening tonight"?. Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Will it be cold tonight?". Expected output: YES.
    -> User: "Can I still buy places for tonight's play?". Expected output: YES.
    -> User: "Are there any spots for my motorbike near the theatre?". Expected output: YES.

"""

prefix_relevanceCheckConfirmation = """
    If the message you will see under </SYS> indicates that I am happy and agree, respond with 'YES'

    If the message you will see under </SYS> indicates that I am unhappy or disagree with something said to me, there are 2 options:
    - If the message explains why I disagree or what I want to change about something said previously, respond with 'YES'
    - If the message does NOT explain why I disagree or what I want to change about something said previously, respond with a reminder that I should explain why I disagree.
"""


def checkRelevance(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"checkRelevance with {(message, status, notepad)}")

    prompt = ""
    if status == 'START':
        prompt = construct_prompt(message, prefix_relevanceCheckStart)
    if status == "FUNCTIONS" or status == "STRUCTURE":
        prompt = construct_prompt(message, prefix_relevanceCheckConfirmation)
    
    output = getModelOutput(prompt, logger)

    notepad['user_requests'] += "- " + message + "\n"

    return (output, status, notepad)