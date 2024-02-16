from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from llama_cpp import Llama

# model_path = "./llama-2-7b-chat.Q2_K.gguf"


examples = [
    {
        "query": "i want a parking lot, then go to an event if the weather condition will be sunny",
        "answer": '["YES",["parking recommendation", "event booking", "weather checking"],"i want a parking lot, then go to an event if the weather condition will be sunny"]'
    },
    {
        "query": "I'm searching my soulmate",
        "answer": '["NO",[],"I\'m sorry, but the request i\'m searching my soulmate does not relate to any of the topics supported by this app. We expect requests to be related to topics such as parking advice, ticket availability, weather check, or event booking. For example, you could ask for recommendations on parking near the event venue or inquire about the availability of tickets for specific events. Please provide a request that falls within the supported topics so that we can assist you effectively."]'
    },
    {
        "query":"I want to park my car near the city's castle",
        "answer": '["YES",["parking recommendation"],"I want to park my car near the city\'s castle"]'
    },
    {
        "query":"I want to travel around L'Aquila",
        "answer": '["NO",[],"While we appreciate your interest in exploring L\'Aquila, the request I want to travel around L\'Aquila does not specify a topic supported by this app. To better assist you, we recommend making requests related to specific aspects of your travel within L\'Aquila, such as parking advice, ticket availability for local events, weather forecasts, or booking accommodations for upcoming events. For example, you could inquire about the availability of parking near tourist attractions or ask for recommendations on local events happening during your visit. Please provide a request that falls within the supported topics so that we can assist you effectively."]'
    },
    {
        "query":"I want to see which events are avaiable",
        "answer": '["YES",["ticket availability", "event booking"],"I want to see which events are avaiable"]'
    },
    {
        "query":"Will it rain in L'Aquila?",
        "answer": '["YES",["weather checking"],"Will it rain in L\'Aquila?"]'
    },
    {
        "query":"If it doesn't rain I want to go to Rome",
        "answer": '["NO",[],"We understand your interest in planning your trip, but the request If it doesn\'t rain I want to go to Rome does not align with the supported topics of this app. To better assist you, we recommend making requests related to specific interess related to the Street Science in L\'Aquila . For example, you could inquire about parking options for your departure or ticket availability for events. Alternatively, you could ask for weather forecasts to plan your schedule. Please provide a request that falls within the supported topics so that we can assist you effectively."]'
    },
    {
        "query":"I'm feeling alone",
        "answer": '["NO",[],"We appreciate your willingness to engage, but the request I\'m feeling alone does not pertain to any of the supported topics of this application. To best assist you, we encourage requests that are relevant to the specified topics, such as seeking parking advice, checking ticket availability for events, obtaining weather forecasts, or making bookings for upcoming events. For instance, you could ask about parking options for an event you plan to attend, inquire about ticket availability for a local concert, or request information about upcoming weather conditions. Please provide a request related to one of the supported topics so that we can provide you with accurate assistance."]'
    },
    {
        "query":"i want to know how to be a better person",
        "answer" : '["NO",[],"We appreciate your interest. However, the request I want to know how to be a better person does not align with the supported topics provided by this application. To receive optimal assistance, we encourage inquiries that are relevant to the designated topics, such as seeking parking advice, checking ticket availability for events, obtaining weather forecasts, or making bookings for upcoming events. For example, you could inquire about parking options for an event you plan to attend, check ticket availability for a specific Street Science event, or request information about upcoming weather conditions. Please submit a request related to one of the supported topics to facilitate accurate assistance."]'
    },
]


# example_template = """
#     User:{query},
#     AI:{answer}
# """

# example_prompt = PromptTemplate(
#     input_variables=["query", "answer"],
#     template=example_template
# )

prefix= """
    Given the user input and based on the context, identify the intents from the following list: 
    ["parking recommendation", "ticket availability", "weather checking", "event booking"]. What is meant by intent is what the user is reauesting. 
    The user has been instructed to make a request based on the following description: 'This app is used during the street science days in L'Aquila. Please make requests relating to the following topics: [parking advice, ticket availability, weather check, event booking].'
    The number of intents can range from 0 to 4 and an intent should not be repeated.
"""

suffix="""
    Respond based on the following intent: {query},
"""

# few_shot_template = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     prefix=prefix,
#     suffix=suffix,
#     input_variables=["query"],
#     example_separator="\n\n"
# )

# llm = Llama(model_path=model_path)
# chain = LLMChain(llm=llm, prompt=few_shot_template, verbose=0)


def construct_system_message(
    prefix: str, 
    examples: dict[str, str],
    suffix: str,
) -> str:
    system_message = prefix + "\n"
    # system_message += "Here are some examples:\n\n"
    # for example in examples:
    #     system_message += f"User: {example['query']}\n"
    #     system_message += f"AI: {example['answer']}\n\n"
    system_message += suffix
    return system_message
    

def construct_prompt(user_message: str, system_message: str = " ") -> str:
    assert(system_message != None)
    assert(system_message != "")

    return f"""<s>[INST] <<SYS>>
        {system_message}
        <</SYS>> 
        {user_message} [/INST]"""

def invokeChatbot(message: str):
    max_tokens = 100
    model_path = "./llama-2-7b-chat.Q2_K.gguf"

    suffix= f"""
        Respond based on the following intent: {message},
    """
    system_message = construct_prompt(message, construct_system_message(prefix, examples, suffix))
    prompt = system_message

    n_ctx = system_message.count(' ')*2 + max_tokens
    print(n_ctx)
    model = Llama(model_path=model_path, n_ctx=n_ctx)

    output = model(prompt, max_tokens=max_tokens, echo=True)
    return output
    