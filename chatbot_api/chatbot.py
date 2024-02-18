from llama_cpp import Llama
import re

def extract_text_between_brackets(text):
    # This pattern matches the text between the first set of square brackets
    match = re.search(r'\[(.*?)\]', text)
    if match:
        # Return the first group of the match
        return match.group(1)
    else:
        # Return None if no brackets are found
        return None

# model_path = "./llama-2-7b-chat.Q2_K.gguf"


# prefix= """
#     Given the user input after </SYS>, identify the user's intents / user goals. If any of the intents in the following list are implied by the user, add this intent to your response list: 
#     ["parking recommendation", "ticket availability", "weather checking", "event booking"]. 
#     The user has been instructed to make a request based on the following description: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking advice, ticket availability, weather check, event booking].'
#     The number of intents identified by you can range from 0 to 4 and an intent should not be repeated.
# """

prefix_relevanceCheck= """
    Given the user input, determine if the request aligns with one of the following specified intents:

    Intents:
    
    - 'parking recommendation': Indicates the user wants to know where to park their vehicle, they will ask for a location.
    - 'ticket availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather checking': Indicates the user wants to know about the current weather or temperature.
    - 'event booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.
    
    Context: This service is tailored for attendees of the Street Science days in L'Aquila. Users are encouraged to make requests related to parking, ticketing for events, weather information, or event bookings only.

    Your task is to analyze the user's input and identify whether it falls within the specified intents. If the input does not align with these intents, or includes requests outside the specified categories, instruct the user to refine their query according to the available services.

    Output Guidelines:
    Your response must strictly be one of the following, based on the user's input. Do not include any additional explanations, greetings, or any text beyond what is specified here.

    - If all parts of the user's request fall within the specified intents, respond with 'OK'.
    - If any part of the request is outside the specified intents, respond with: "What can I help you with? Your request should be one or multiple intents falling under the four listed above."

    Ensure that your output matches one of these two options, word for word.

    Example User Inputs and Expected Responses:
    -> User: "How old am I?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Can I pet my dog?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I want to visit Rome". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I want to buy a car". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Where is my sandwich?". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "I feel lonely". Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Where is the concert happening tonight"?. Expected output: What can I help you with? Your request should be one or multiple intents falling under the four listed above.
    -> User: "Will it be cold tonight?". Expected output: OK.
    -> User: "Can I still buy places for tonight's play?". Expected output: OK.
    -> User: "Are there any spots for my motorbike near the theatre?". Expected output: OK.

"""

prefix_functionIdentification= """
    The user input you will get after </SYS> will be one or multiple of the intents stated in the below list.
    
    Intents:
    - 'parking recommerndation': Indicates the user wants to know where to park their car, they will ask for a location.
    - 'ticket availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather checking': Indicates the user wants to know about the current weather or temperature.
    - 'event booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.
    
    The user has been instructed to make a request based on the following context: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking recommendation, ticket availability, weather checking, event booking].'
    
    Instructions:
    1. Analyze the user input to determine which intents are present.
    2. Consider the context to understand the underlying meaning of the user input.
    3. Output the identified intents in a list and no other explanation.


    The number of intents identified by you can range from 0 to 4 and an intent should not be repeated.

    Output Guidelines:
    Your response must strictly be one of the following format, based on the user's input. Do not include any additional explanations, greetings, or any text beyond what is specified here. The format can be like a python list, where each identified intent is an element seperated by commas, and all elements are placed between square brackets.

"""

prefix_identifyLogicalOperations= """
    Given the message(s) after </SYS>, identify the relationships between the intents listed after </SYS>. If any of the relationships in the following list are implied by the user, add this relationship to your response list.
    
    Relationship:
    [Choose one of the following options: AND, OR, ONE_OF, SEQ]
 
    Explanation:
    - 'AND': Indicates all actions are desired, showing an additive relationship. Both intents must be fulfilled.
    - 'OR': Suggests a choice between actions, where one or the other (or one of several) is desired. Only one of the intents needs to be fulfilled.
    - 'ONE_OF': Specifies a choice of exactly one action from a list of up to four. Only one intent should be chosen.
    - 'SEQ': Indicates a sequence of actions, where the order of actions is important based on the context, not necessarily the order they are mentioned in the sentence. One intent must be completed before the other.
 
    
    The user has been instructed to make a request based on the following context: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking advice, ticket availability, weather check, event booking].'
    
    Instructions:
    1. Analyze the user input to identify the relationship.
    2. Consider the context to understand the underlying meaning of the user input.
    3. Output the identified relationship.
 
    The number of relationship identified by you can range from 0 to 1.
 
    Please identify the relationship present in the text:
 
"""

prefix_askFunctionCorrect = """
    After </SYS> you are presented a list of intents. These intents have been identified from a user's request. 

    These intents can be the following:
    - 'parking recommendation': Indicates the user wants to know where to park their vehicle, they will ask for a location.
    - 'ticket availability': Indicates the user wants to know if there are free places to the event they want to attend.
    - 'weather checking': Indicates the user wants to know about the current weather or temperature.
    - 'event booking': Indicates the user wants to participate to a gathering by purchasing a billet. The gathering can be a concert, sport event, festival, play or exhibition.

    You should use the user if the presented intents after </SYS> are correctly identified.
    Only ouput the question.
"""

examples_logicalOperators = [
    {
        'functions': "",
        'user_requests': "", 
        'output': ""
    },
]

# ------------- vars ------------------
max_tokens = 300
model_path = "./llama-2-13b-chat.Q2_K.gguf"

def getModelBasedOnInput(prompt: str, logger):
    n_ctx = prompt.count(' ')*2 + max_tokens
    logger(n_ctx)
    return Llama(model_path=model_path, n_ctx=n_ctx, echo=False)




# -------------- functions --------------------


def construct_prompt(user_message: str, prefix: str = " ") -> str:
    assert(prefix != None)
    assert(prefix != "")

    return f"""<s>[INST] <<SYS>>
        {prefix}
        <</SYS>> 
        {user_message} [/INST]"""



def invokeChatbot(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"invokeChatbot with {(message, status, notepad)}")
    # note status

    return checkRelevance(message, status, notepad, logger)
    

def checkRelevance(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"checkRelevance with {(message, status, notepad)}")

    prompt = construct_prompt(message, prefix_relevanceCheck)
    model = getModelBasedOnInput(prompt)

    output = model(prompt, max_tokens=max_tokens, echo=False)

    extracted_text : str = output["choices"][0]["text"]

    notepad['user_requests'] += "- " + message + "\n"

    if extracted_text.__contains__('OK'):
        logger(f"OK")
        return identifyFucntions(message, status, notepad, logger)

    logger(f"Not OK: {(extracted_text, status, notepad)}")
    return (extracted_text, status, notepad)



def identifyFucntions(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"identifyFucntions with {(message, status, notepad)}")

    prompt = construct_prompt(notepad['user_requests'], prefix_functionIdentification)
    model = getModelBasedOnInput(prompt, logger)

    output = model(prompt, max_tokens=max_tokens, echo=False)

    extracted_text : str = output["choices"][0]["text"]
    pattern = r'\[(.*?)\]'
    functionsList = re.findall(pattern, extracted_text)[0]
    # functionsList = extract_text_between_brackets(extracted_text)

    notepad['functions'] = functionsList
    
    status = 'FUCNTIONS'

    return (notepad['functions'], status, notepad)
    # return askFunctionsCorrect(extracted_text, status, notepad, logger)


def askFunctionsCorrect(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"askFunctionsCorrect with {(message, status, notepad)}")

    prompt = construct_prompt(notepad['functions'], prefix_askFunctionCorrect)
    logger(f"t0, {prompt}")
    model = getModelBasedOnInput(prompt, logger)
    logger("t1")
    output = model(prompt, max_tokens=max_tokens, echo=False)
    logger("t2")

    extracted_text : str = output["choices"][0]["text"]
    
    return (extracted_text, status, notepad)


def generateMessageLogicalOperators(functions: str, user_requests: str) -> str:
    message =  f"The identified intents are: {functions}\n"
    return f"{message}The user's message(s) that has to be parsed for determining relationships between intents are: \n {user_requests}\n\n"

def generatePrefixLogicalOperators(examples: list[dict[str, str]]) -> str:
    prefix = prefix_identifyLogicalOperations
    prefix += '\nHere are some examples of input you can receive and what you should ouput based on that input.\n'
    for i in range(len(examples)):
        prefix += f"example {i}:\n - "
        prefix += generateMessageLogicalOperators(examples[i]['functions'], examples[i]['user_requests'])
        i += 1
    return prefix


def identifyLogicalOperators(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"identifyLogicalOperators with {(message, status, notepad)}")

    message = "The identified intents are: " + notepad['functions'] + "\n\n"
    message += f"The user's message(s) that has to be parsed for determining relationships between intents are: \n {notepad['user_requests']}"

    prompt = construct_prompt(
        generateMessageLogicalOperators(
            notepad['functions'], 
            notepad['user_requests']
        ), 
        generatePrefixLogicalOperators(examples_logicalOperators),
    )

    model = getModelBasedOnInput(prompt, logger)
    output = model(prompt, max_tokens=max_tokens, echo=False)

    extracted_text : str = output["choices"][0]["text"]

    status = 'STRUCTURE'
    
    return (extracted_text, status, notepad)