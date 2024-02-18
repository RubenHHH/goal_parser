from .util import getModelOutput, construct_prompt


prefix_askFunctionCorrect = """
After </SYS> you are presented a list of my goals.

These goals can be the following:
- 'parking_recommendation': Indicates the user wants to know where to park their vehicle, they will ask for a location.
- 'ticket_availability': Indicates the user wants to know if there are free places to the event they want to attend.
- 'weather_checking': Indicates the user wants to know about the current weather or temperature.
- 'event_booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.

Act like you identified the list of goals yourself and ask me if you identified them correcly. Do this in a natural language way, I don't want to see underscores.
Do NOT tell me you looked through the list and do NOT tell me something like 'Sure, here it is'.
Only ask me the question.
"""


def askFunctionsCorrect(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"askFunctionsCorrect with {(message, status, notepad)}")

    prompt = construct_prompt(notepad['functions'], prefix_askFunctionCorrect)
    output = getModelOutput(prompt, logger)

    output += "\nPlease either confirm or explain why you think I identified your intentions incorrectly"
    
    return (output, status, notepad)