from .util import getModelOutput, construct_prompt


# prefix_identifyLogicalOperations= '''
#     Given the user's message(s) after </SYS>, identify the relationships between the already identified intents listed after </SYS>.
    
#     Relationship:
#     - Relationships can be the following: 'and', 'or', 'one_of', 'seq'
#     - Relationships can describe the connections between the intents specified after </SYS>
#     - Relationships can describe the connection between connected intents as explained above
 
#     Explanation:
#     - 'and': Indicates that its surrounding intents are desired, showing an additive relationship.
#     - 'or': Suggests a choice between its surrounding intents, where one or the other (or one of several) is desired.
#     - 'one_of': Specifies a choice of exactly one desired intent from a list of intents.
#     - 'seq': Indicates a sequence of desired intents, where the order of actions is important based on the context, not necessarily the order at which they are mentioned in the sentence.
    
#     Output rules:
#     - Do NOT output anything other than the intents and their relationships
#     - Structure the relationships as follows ('INTENT_OR_RELATED_INTENTS' is a placeholder value for identied intents or relationships between them, and '...' is a placeholder value for a continuation of the same pattern):
#         - 'and': '[INTENT_OR_RELATED_INTENTS and INTENT_OR_RELATED_INTENTS and ...]'
#         - 'or: '[INTENT_OR_RELATED_INTENTS or INTENT_OR_RELATED_INTENTS or ...]'
#         - 'one_of': 'one of [INTENT_OR_RELATED_INTENTS ; INTENT_OR_RELATED_INTENTS ; INTENT_OR_RELATED_INTENTS ; ...]'
#         - 'seq': 'seq [INTENT_OR_RELATED_INTENTS ; INTENT_OR_RELATED_INTENTS ; ...]'
#     - The whole output should conform to the rules
#     - Your response must strictly be one of the given format, based on the user's input. Do not include any additional explanations, greetings, or any text beyond what is specified here.
#     - Minimize how verbose your output is. Your input should start with '[' and end with ']', which means that you should NOT mention which operators you have identified seperately.
# '''

prefix_identifyLogicalOperations = """
Task Instruction:
 
Your objective is to analyze user requests (between <<< and >>> after </SYS>) and accurately identify logical relationships between specified intents. These relationships can be expressed using four logical operators: `and`, `or`, `one_of`, and `seq`. Your response must strictly adhere to a predefined format that may involve nesting these operators to reflect complex intent relationships. Draw inspiration from provided examples to understand how to apply and structure these logical operators. The output should be concise, directly addressing user intent, without any additional explanations or text outside the specified format.
 
Logical Operators:
 
- `and`: Connects intents with an additive relationship, which means that the order is not important.
- `or`: Indicates a choice between intents, where any one or more could be desired.
- `one_of`: Specifies a choice of exactly one intent from a list.
- `seq`: Describes a sequence of intents, highlighting the importance of order.
 
Keywords that should be mapped to logical operators:
- `and`: `and`, `both...and`, `all of...`, `in addition...`
- `or`: `or`, `choose among...`
- `one_of`: `only`, `one of...`, `only...or`, `either...or`
- `seq`: `first ... then`, `in the order of`, `if...then`, `in sequence...`, `before`, `after`

Nesting Logical Operators:
 
Operators can be nested within each other to represent complex intent relationships. For example, an intent can be desired in conjunction with one of several other intents (`[intent1 and [intent2 or intent3]]`), or there may be a sequence where one step depends on choosing one of several options (`seq [intent1; one_of[intent2; intent3]]`).
 
Output Format:
 
Your response must strictly conform to the provided structure, starting with `+++[` and ending with `]===`, encapsulating the identified intents and their logical relationships.
Examples of correct format include:
- `+++[`intent1` and `intent2`]===`
- `+++[one_of [`intent1`; `intent2`; `intent3`]]===`
- `+++seq [`intent1`; `intent2`]===`
- `+++[`intent1` or `intent2`]===`
- `+++[[`intent1` and `intent2`] or `intent3`]===`
- `+++seq [[`intent1` or `intent2`] ; `intent3`]===`
- `+++one_of [`intent1` ; [`intent2` or `intent3`]]===`

Note that you have a preference for choosing the 'and' operator, so you have to be absolutely sure that the relationship between intents is 'and'. Choosing 'or', 'seq', 'one_of' is more likely.
 
Drawing Inspiration from Examples:
 
The provided examples are key to understanding how to apply these rules in practice. Each example demonstrates the application of logical operators, their potential for nesting, and the precise output format required. Ensure your outputs align with these examples in both structure and clarity.
 
Directing Output Towards User Intent:
 
Your output is directed towards understanding and addressing user intent as specified in their requests (between <<< and >>> after </SYS>). It should be laser-focused on identifying and structuring the logical relationships between intents, following the strict guidelines provided. Avoid including any additional information, greetings, or clarifications outside of the required format, as your output will be directly passed to the user.
"""

examples_logicalOperators = [
    # {
    #     'functions': "weather_checking, parking_recommendations, ticket_availability",
    #     'user_requests': "I want to know the weather today and parking_recommendations or check ticket_availability for tonight\'s concert.",
    #     'output': "[ 'weather_checking' and ['parking_recommendation' or 'ticket_availability']]"
    # },
    # {
    #     'functions': "weather_checking, ticket_availability, parking_recommendation",
    #     'user_requests': "I need the tickets to the exhibition if the weather is warm and nice and also provide parking_recommendations",
    #     'output': "seq ['weather_checking' ; 'ticket_availability']  and 'parking_recommendation'"
    # },
    # {
    #     'functions': "weather_checking, parking_recommendations, ticket_availability, event_booking",
    #     'user_requests': "Provide one the following information, details regarding the weather today, place to park my card, tickets to the show tonight. Also provide event_booking details for the show.",
    #     'output': "one_of'[weather_checking' ; 'parking_recommendation' ; 'ticket_availability'] and 'event_booking'"
    # },
    # {
    #     'functions': "ticket_availability, event_booking, weather-checking",
    #     'user_requests': "I want to know the ticket_availability or event_booking details and the information regarding the weather today",
    #     'output': "[['ticket_availability' or 'event_booking'] and 'weather_checking']"
    # },
    # {
    #     'functions': "ticket_availability, parking_recommendation",
    #     'user_requests': "I need to know if tickets are available to the concert and also please recommend good parking spots",
    #     'output': "['ticket_availability' and 'parking_recommendation']"
    # },
    # {
    #     'functions': "weather_checking, parking_recommendation",
    #     'user_requests': "Please check the weather and also recommend good parking spots",
    #     'output': "['weather_checking' and 'parking_recommendation']"
    # },
    # {
    #     'functions': "event_booking, ticket_availability",
    #     'user_requests': "I want to know the details regarding the event tonight or some information regarding ticket_availability",
    #     'output': "['event_booking' or 'ticket_availability']"
    # },
    # {
    #     'functions': "ticket_availability, weather_checking",
    #     'user_requests': "First, I need to know the ticket_availability and then the weather outside ",
    #     'output': "seq ['ticket_availability' ; 'weather_checking']"
    # },
    # {
    #     'functions': "event_booking, weather_checking",
    #     'user_requests': "Provide information regarding the event tonight if the weather is good outside",
    #     'output': "seq ['weather_checking' ; 'event_booking']"
    # },
    # {
    #     'functions': "weather_checking, ticket_availability, parking_recommendation",
    #     'user_requests': "I want to know the weather information today and check if the tickets are available for the concert tonight or provide good parking spots close to me",
    #     'output': "[['weather_checking' or 'ticket_availability'] and 'parking_recommendation']"
    # },
    # {
    #     'functions': "parking_recommendation, ticket_availability, event_booking",
    #     'user_requests': "I want to check the ticket_availability only if there are good parking spots in the area or check the event_booking details if there are available tickets",
    #     'output': "[seq ['parking_recommendation' ; 'ticket_availability'] or seq ['ticket_availability ; 'event_booking']]"
    # },
    # {
    #     'functions': "parking_recommendation, event_booking, ticket_availability",
    #     'user_requests': "I want either parking_recommendation or event details for the carnival tonight and check if tickets are still available",
    #     'output': "[['parking_recommendation' or 'event_booking'] and 'ticket_availability']"
    # },
    # {
    #     'functions': "weather_checking, event_booking, ticket_availability",
    #     'user_requests': "Provide of the following after checking the weather today, information about the event today, available tickets for the event.",
    #     'output': "[ seq ['weather_checking' ; one_of['event_booking' ; 'ticket_availability']]]"
    # },
    # {
    #     'functions': "weather_checking, ticket_availability, event_booking",
    #     'user_requests': "I want to check if the tickets are available if the weather is good outside and I want to check the event_booking details if there are good parking spots in the area",
    #     'output': "[seq ['weather_checking' ; 'ticket_availability'] and seq ['parking_recommendation' ; 'event_booking']]"
    # },
    # {
    #     'functions': "weather_checking, parking_recommendation, ticket_availability",
    #     'user_requests': "I want to know the weather outside and check if there are good parking spots nearby or check if tickets are available to the concert tonight",
    #     'output': "['weather_checking' and ['parking_recommendation' or 'ticket_availability']]"
    # },
    # {
    #     'functions': " parking_recommendation, ticket_availability, event_booking",
    #     'user_requests': "I want to check the ticket_availability but first check if there are good parking spots nearby. Also provide the details regarding event_booking for the festival this weekend",
    #     'output': "[ seq [ 'parking_recommendation' ; 'ticket_availability' ] and 'event_booking' ]"
    # },
    # {
    #     'functions': " weather_checking, ticket_availability, event_booking, parking_recommendation",
    #     'user_requests': "I want to check the weather outside and get event_booking information if there are available tickets and also check if there are good parking spots nearby",
    #     'output': "[ 'weather_checking' and seq [ 'event_booking' ; 'ticket_availability' ] and 'parking_recommendation' ]"
    # },
    # {
    #     'functions': " parking_recommendation, ticket_availability, weather_checking, event_booking",
    #     'user_requests': "I want to check the parking_recommendation nearby or check if tickets are available to the festival if the weather is nice outside or provide information regarding event_booking this weekend",
    #     'output': "[ 'parking_recommendation' and seq [ 'ticket_availability' ; 'weather_checking' ] and 'event_booking' ]"
    # },
    # {
    #     'functions': " ticket_availability, event_booking, weather_checking, parking_recommendation",
    #     'user_requests': "Provide one of the following: check the event_booking details if the tickets are available, check good parking spots if the weather is nice outside",
    #     'output': "one_of [  seq [ 'ticket_availability' ; 'event_booking'] ;  seq [ 'weather_availability' ; 'parking_recommendation']]"
    # },
    # {
    #     'functions': "weather_checking, event_booking, parking_recommendation",
    #     'user_requests': "I want to check the weather outside or provide event_booking details or check for good parking spots nearby",
    #     'output': "[ 'weather_checking' or 'event_booking' or 'parking_recommendation' ]"
    # },
    # {
    #     'functions': "ticket_availability, event_booking, parking_recommendation",
    #     'user_requests': "I need to buy the tickets for tonight's festival if I am sure that I can leave my bike in a safe space.",
    #     'output': "seq ['parking_recommendation'; 'ticket_availability'; 'event_booking']"
    # },
    # {
    #     'functions': "ticket_availability, event_booking, weather_checking, parking_recommendation",
    #     'user_requests': "I would like to book tickets for the event tonight. But first, check if is hot enough and where I can leave my motorbike",
    #     'output': "seq [['weather_checking' and 'parking_recommendation']; 'ticket_availability'; 'event_booking']"
    # },
    # {
    #     'functions': "parking_recommendation, ticket_availability, weather_checking",
    #     'user_requests': "I want to do one of the following: either check where i can park my car, know if there are places available for the play tonight or check the weather forecast",
    #     'output': "one_of ['parking_recommendation'; 'ticket_availability'; 'weather_checking']"
    # },
    # {
    #     'functions': "weather_checking, ticket_availability, parking_recommendation",
    #     'user_requests': "Please tell me if it will be cold tomorrow or tell me if there are places left for the party tomorrow night or if I can leave my car somewhere",
    #     'output': "['weather_checking' or 'ticket_availability' or 'parking_recommendation']"
    # }, 
    # {
    #     'functions': "parking_recommendation, weather_checking, ticket_availability, event_booking",
    #     'user_requests': "Make sure I will find a spot for my minivan and that I won't be cold and that I have my tickets to attend the show",
    #     'output': "['parking_recommendation' and 'weather_checking' and seq ['ticket_availability'; 'event_booking']]"
    # },
    # {
    #     'functions': "weather_checking, ticket_availability, parking_recommendation",
    #     'user_requests': "I want to first do one of the following: check if the weather will be nice tonight or if I can still attend the dance recital and then check where i can park my car.",
    #     'output': "seq [one_of ['weather_checking'; 'ticket_availability']; 'parking_recommendation']"
    # },
    # {
    #     'functions': "weather_checking, parking_recommendation, ticket_availability",
    #     'user_requests': "Let me do one of the following: first check if it will be sunny then if I can leave my car somewhere or first tell me if I can park my car somewhere and then check for available tickets for tonight's concert",
    #     'output': "one_of [seq ['weather_checking'; 'parking_recommendation']; seq ['parking_recommendation'; 'ticket_availability']]"
    # },
    # {
    #     'functions': "weather_checking, parking_recommendation, ticket_availability, event_booking",
    #     'user_requests': "I would like to do one and only one of these tasks: either first know if it will be cold outside then tell me if you know any spot near the event for my car and then find out if i can still attend the event or check where i can park my car and book an event",
    #     'output': "one_of [seq ['weather_checking'; 'parking_recommendation'; 'ticket_availability']; ['parking_recommendation' and 'event_booking']]"
    # },
    # {
    #     'functions': "ticket_availability, weather_checking, parking_recommendation",
    #     'user_requests': "Can you tell me which events still have free places for me and my friends? In addition, I would like you to tell me if I need to wear a jacket tonight and where I can find a parking spot",
    #     'output': "['ticket_availability' and 'weather_checking' and 'parking_recommendation']"
    # },
    # {
    #     'functions': "ticket_availability,  parking_recommendation, event_booking, weather_checking",
    #     'user_requests': "I want to know if I can first know if there are tickets available for tonight or if I can leave my car near and then if I can book the tickets for the event or know the forecasted temperatures",
    #     'output': "seq [['ticket_availability' or 'parking_recommendation']; ['event_booking' or 'weather_checking']]"
    # },
    # {
    #     'functions': "parking_recommendation, ticket_availability, weather_checking",
    #     'user_requests': "After I know if I can park my car and if I can attend the event in two days, can you tell me the temperature predictions?",
    #     'output': "seq [['parking_recommendation' and 'ticket_availability']; 'weather_checking']"
    # },
    # {
    #     'functions': "event_booking, weather_checking, parking_recommendation",
    #     'user_requests': "I want to do one of the following: either book the event for tomorrow and check the weather or check for the weather forecast and park my car",
    #     'output': "one_of [['event_booking' and 'weather_checking']; ['weather_checking' and 'parking_recommendation']]"
    # },
    # {
    #     'functions': "parking_recommendation, event_booking, ticket_availability, weather_checking",
    #     'user_requests': "I want to do one of the following: check for parking spots and get to know the booking modalities for the event or check if there are free places for the concert and see if I can wear my skirt or if I will be too cold",
    #     'output': "one of [['parking_recommendation' and 'event_booking']; ['ticket_availability' and 'weather_checking']]"
    # },
    # {
    #     'functions': "weather_checking, event_booking, ticket_availability, parking_recommendation",
    #     'user_requests': "I need to check the weather or buy the tickets and look for availabilities or check for parking_recommendation",
    #     'output': "[['weather_checking' or 'event_booking'] and ['ticket_availability' or 'parking_recommendation']]"
    # },
    # {
    #     'functions': "ticket_availability, event_booking, weather_checking, parking_recommendation",
    #     'user_requests': "I need to do one of the following: check for available billets for the match or book the places and check first how cold it will be tonight and then where i can park my car ",
    #     'output': "[one of['ticket_availability'; 'event_booking'] and [seq['weather_checking'; 'parking_recommendation']]]"
    # },
    # {
    #     'functions': "ticket_availability, weather_checking, parking_recommendation",
    #     'user_requests': "Can you tell me the answer of only one of the requests I am going to make: tell me how many places left there are to the event, check whether it will be more windy or rainy and tell me the available parking lots near the event",
    #     'output': "one_of ['ticket_availability'; 'weather_checking'; 'parking_recommendation']"
    # },
    # {
    #     'functions': "parking_recommendation, ticket_availability",
    #     'user_requests': "Maybe I should check if I it going to be crowded tonight for my car or I should check the availability first",
    #     'output': "['parking_recommendation' or 'ticket_availability']"
    # },
    # {
    #     'functions': "ticket_availability, parking_recommendation, event_booking",
    #     'user_requests': "Tell me if I can still attend the play tonight before checking for parking spots and booking information",
    #     'output': "seq ['ticket_availability'; ['parking_recommendation' and 'event_booking']]"
    # },
]



def _generateMessageLogicalOperators(functions: str, user_requests: str) -> str:
    message =  f'The identified intents are: \n - {functions}\n\n'
    return f"{message}The user's message(s) that have to be analyzed for determining relationships between intents are: <<<\n{user_requests}>>>\n"


def identifyLogicalOperators(message: str, status: str, notepad: dict[str, str], logger):
    logger(f'identifyLogicalOperators with {(message, status, notepad)}')

    prompt = construct_prompt(
        _generateMessageLogicalOperators(
            notepad['functions'], 
            notepad['user_requests']
        ), 
        prefix_identifyLogicalOperations
    )

    logger(prompt)

    output = getModelOutput(prompt, logger)

    userGoals = extract_string_within_square_brackets(output)

    status = 'STRUCTURE'
    
    return (userGoals, status, notepad)



def extract_string_within_square_brackets(input_string: str):
    end_index = input_string.rfind(']==')
    start_index = input_string.rfind('++[')
    
    if start_index == -1 or end_index == -1:
        return None  # No square brackets found
    
    return input_string[start_index+2:end_index +1]