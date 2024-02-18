from llama_cpp import Llama
import sys
import os

class DisablePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = sys.stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr




max_tokens = 300
model_path = "./llama-2-13b-chat.Q2_K.gguf"


def getModelOutput(prompt: str, logger):
    n_ctx = int(prompt.count(' ')*2) + max_tokens

    logger(f'context window: {n_ctx}')
    with DisablePrint():
        model = Llama(model_path=model_path, n_ctx=n_ctx, echo=False)
        output = model(prompt, max_tokens=max_tokens, echo=False)
        extracted_text : str = output["choices"][0]["text"]
    logger(f"model out: {extracted_text}")
    return extracted_text



def construct_prompt(user_message: str, prefix: str = " ") -> str:
    assert(prefix != None)
    assert(prefix != "")

    return f"""<s>[INST] <<SYS>>
        {prefix}
        <</SYS>> 
        {user_message} [/INST]"""