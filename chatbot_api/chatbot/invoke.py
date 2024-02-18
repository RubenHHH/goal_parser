from .checkRelevance import checkRelevance

def invokeChatbot(message: str, status: str, notepad: dict[str, str], logger):
    logger(f"invokeChatbot with {(message, status, notepad)}")
    # note status

    return checkRelevance(message, status, notepad, logger)