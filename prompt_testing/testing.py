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







def construct_prompt(user_message: str, prefix: str = " ") -> str:
    assert(prefix != None)
    assert(prefix != "")

    return f"""<s>[INST] <<SYS>>
        {prefix}
        <</SYS>> 
        {user_message} [/INST]"""

max_tokens = 300
model_path = "../chatbot_api/llama-2-13b-chat.Q2_K.gguf"
def getModelBasedOnInput(prompt: str):
    with DisablePrint():
        n_ctx = (prompt.count(' '))*2 + max_tokens
        model = Llama(model_path=model_path, n_ctx=n_ctx, echo=False)
    return model



# --------------- Uncomment if you want manual input -------------------------


while(True):
    prefix = input("Enter prefix:\n")
    message = input('Enter message:\n')

    prompt = construct_prompt(message, prefix)
    model = getModelBasedOnInput(prompt)

    output = model(prompt, max_tokens=max_tokens, echo=False)

    extracted_text : str = output["choices"][0]["text"]

    print("\n")
    print(extracted_text)


# -------------------------------------------------------------------------------------

# --------------- Uncomment if you want to use hardcoded prefixes and messages -------------------------


# prefix = "Refuse to answer"
# message = "What is my name?"

# prompt = construct_prompt(message, prefix)
# model = getModelBasedOnInput(prompt)

# print("test")
# output = model(prompt, max_tokens=max_tokens, echo=True)
# print("testt")

# extracted_text : str = output["choices"][0]["text"]

# print("\n")
# print(extracted_text)


# -------------------------------------------------------------------------------------