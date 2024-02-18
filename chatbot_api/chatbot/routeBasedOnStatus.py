
from .identifyFunctions import identifyFunctions
from .identifyLogicalOperators import identifyLogicalOperators

def routeBasedOnStatus(message: str, status: str, notepad: dict[str, str], logger):

    if status == "START" or status == "FUNCTIONS-bad":
        return identifyFunctions(message, status, notepad, logger)

    if status == "FUNCTIONS-good" or status == "STRUCTURE-bad":
        return identifyLogicalOperators(message, status, notepad)

    # if status == 'STRUCTURE-good':
        # mapToGrammar(message, status, notepad)
