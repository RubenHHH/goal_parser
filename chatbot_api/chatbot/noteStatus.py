from .util import getModelOutput, construct_prompt


prefix_noteStatus = """
I received feedback from an AI. You can see my response to the feedback after </SYS>.

Do one of the following cases:
- If you identify that I confirmed that the feedback is correct, respond with 'YES'
- If you identify that I'm not fully satisfied with the feedback, respond with 'NO'

Do not output/respond with anything other than 'YES' or 'NO'
"""

def noteStatus(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"noteStatus with {(message, status, notepad)}")

    if status == 'START' or status == 'DONE':
        return (message, status, notepad)
    
    prompt = construct_prompt(message, prefix_noteStatus)
    output = getModelOutput(prompt, logger)

    if (status == 'FUNCTIONS' or status == 'STRUCTURE') and output.__contains__('YES'):
        status += '-good'
    if (status == 'FUNCTIONS' or status == 'STRUCTURE') and output.__contains__('NO'):
        status += '-bad'
    
    return (message, status, notepad)
