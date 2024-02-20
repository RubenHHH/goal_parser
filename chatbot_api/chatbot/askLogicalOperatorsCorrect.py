from .util import getModelOutput, construct_prompt


prefix_askLogicalOperatorsCorrect = """
After </SYS> you are presented some of my goals in a structure of `and`s, `or`s, `seq`s, and/or `one_of`s.

The goals can be the following:
- 'parking_recommendation': Indicates that I want to know where to park my vehicle.
- 'ticket_availability': Indicates that I want to know if there are free places to the event I want to attend.
- 'weather_checking': Indicates that I want to know about the current weather or temperature.
- 'event_booking': Indicates that I want to participate in a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.
Look at my some snippets of a previous conversation I had to see what I these goals mean in my case.

This is what the logical operators mean:
- `and`: Connects intents with an additive relationship, which means that the order is not important.
- `or`: Indicates a choice between intents, where any one or more could be desired.
- `one_of`: Specifies a choice of exactly one intent from a list.
- `seq`: Describes a sequence of intents, highlighting the importance of order.

Ask me if you identified the structure of goals correcly as if you were the one who made the structured list. Do this in a natural language way, I don't want to see underscores or parantheses.
Do NOT tell me something like 'I have taken a look at the structured list' and do NOT tell me something like 'Sure, here it is'.
Only ask me the question.

"""


def askLogicalOperatorsCorrect(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"askLogicalOperatorsCorrect with {(message, status, notepad)}")

    message = f"The structured goals:\n{notepad['functions']}\n\nSome conversation snippets:\n{notepad['user_requests']}"

    prompt = construct_prompt(message, prefix_askLogicalOperatorsCorrect)
    output = getModelOutput(prompt, logger)

    output += "\nPlease either confirm or explain why you think I identified the structure of your intentions incorrectly"
    
    return (output, status, notepad)