import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.invoke import invokeChatbot
import ast
import json

# from chatbot import invoke_few_shot_template

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


logging.basicConfig(level=logging.DEBUG,  # Adjust log level as needed
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


LLAMA2_API_URL = "http://your-llama2-api-url.com/predict"


def log(text: str):
    app.logger.info(f"""

    =============================================
    {text}
    =============================================

    """)

@app.route("/api/repeat", methods=["POST"])
def get_response():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json

    if "message" not in data or not isinstance(data["message"], str):
        return jsonify({"error": "JSON must contain the 'message' key with a string value"}), 400

    user_message = data["message"]
    response_message = f"You said '{user_message}' to me"
    return jsonify({"message": response_message})


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    # Put the location of to the GGUF model that you've download from HuggingFace here
    model_path = "./llama-2-7b-chat.Q2_K.gguf"

    # Create a llama model
    model = Llama(model_path=model_path)

    # Prompt creation
    system_message = "You are a helpful assistant"

    prompt = f"""<s>[INST] <<SYS>>
    {system_message}
    <</SYS>>
    {data['message']} [/INST]"""

    # Model parameters
    max_tokens = 100

    # Run the model
    try:
        output = model(prompt, max_tokens=max_tokens, echo=True)
        extracted_text = output["choices"][0]["text"]
        return jsonify({'message': extracted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    log("Entered chatbot API endpoint")

    data = request.json

    log(str(data))

    status = data['status']
    notepad = data['notepad']
    message = data['message']

    if data['status'] == None:
        status = "START"
    else:
        status = data['status']

    if data['notepad'] == None:
        notepad = {
            'user_requests': "",
            'functions': "",
        }
    else:
        notepad = ast.literal_eval(data['notepad'])



    try:
        output, status, notepad = invokeChatbot(message, status, notepad, log)
        # print(str(output))
        log(f"5: {(output, status, notepad)}")
        notepad_json = json.dumps(notepad)
        return jsonify(
            {
                'status': status,
                'notepad': notepad_json,
                'message': output,
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route("/api/chatbot", methods=["POST"])
# def get_response():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     data = request.json

#     if "message" not in data or not isinstance(data["message"], str):
#         return jsonify({"error": "JSON must contain the 'message' key with a string value"}), 400

#     user_message = data["message"]
#     response_message = invoke_few_shot_template(user_message)
#     return jsonify({"message": response_message})
