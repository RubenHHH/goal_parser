from .util import getModelOutput, construct_prompt


prefix_askFunctionCorrect = """
    After </SYS> you are presented a list of intents. These intents have been identified from a user's request. 

    These intents can be the following:
    - 'parking_recommendation': Indicates the user wants to know where to park their vehicle, they will ask for a location.
    - 'ticket_availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather_checking': Indicates the user wants to know about the current weather or temperature.
    - 'event_booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.

    You should use the user if the presented intents after </SYS> are correctly identified.
    Only ouput the question.
"""


def askFunctionsCorrect(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"askFunctionsCorrect with {(message, status, notepad)}")

    prompt = construct_prompt(notepad['functions'], prefix_askFunctionCorrect)
    output = getModelOutput(prompt, logger)
    
    return (output, status, notepad)