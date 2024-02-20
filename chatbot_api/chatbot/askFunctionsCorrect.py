from .util import getModelOutput, construct_prompt


prefix_askFunctionCorrect = """
After </SYS> you are presented a list of my goals and some snippets of a previous conversation I've had.

Act like you identified the list of goals yourself and ask me if you identified them correcly by mentioning EACH of them specifically. Do this in a natural language way, I don't want to see underscores.
Do NOT tell me something like 'I have taken a look at the list' and do NOT tell me something like 'Sure, here it is'.
Only ask me the question.
"""


def askFunctionsCorrect(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"askFunctionsCorrect with {(message, status, notepad)}")

    message = f"The identied goals are:\n - {notepad['functions']}\n\nThe conversation snippets are:\n{notepad['user_requests']}"

    prompt = construct_prompt(notepad['functions'], prefix_askFunctionCorrect)
    output = getModelOutput(prompt, logger)

    output += "\nPlease either confirm or explain why you think I identified your intentions incorrectly"
    
    return (output, status, notepad)