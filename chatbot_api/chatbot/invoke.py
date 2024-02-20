from .checkRelevance import checkRelevance
from .noteStatus import noteStatus
from .identifyFunctions import identifyFunctions
from .askFunctionsCorrect import askFunctionsCorrect
from .identifyLogicalOperators import identifyLogicalOperators
from .askLogicalOperatorsCorrect import askLogicalOperatorsCorrect

def invokeChatbot(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"invokeChatbot with {(message, status, notepad)}")
    
    output, status, notepad = checkRelevance(message, status, notepad, logger)

    if not output.__contains__('YES'):
        return (output, status, notepad)
    
    output, status, notepad = noteStatus(output, status, notepad, logger)

    if status == "START" or status == "FUNCTIONS-bad":
        output, status, notepad = _functionsIdentificationChain(output, status, notepad, logger)

    if status == "FUNCTIONS-good" or status == "STRUCTURE-bad":
        output, status, notepad = _logicalOperatorIdentificationChain(output, status, notepad, logger)

    if status == "STRUCTURE-good":
        status = None
        output = "Our system will handle things from here. You may now make a new request."

    return (output, status, notepad)



def _functionsIdentificationChain(output: str, status: str, notepad: dict[str, str], logger):
    output, status, notepad = identifyFunctions(output, status, notepad, logger)

    return askFunctionsCorrect(output, status, notepad, logger)


def _logicalOperatorIdentificationChain(output: str, status: str, notepad: dict[str, str], logger):
    output, status, notepad = identifyLogicalOperators(output, status, notepad, logger)

    return askLogicalOperatorsCorrect(output, status, notepad, logger)

