import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.identifyLogicalOperators import identifyLogicalOperators

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

    status = None
    notepad = None
    message = data['message']

    if data['status'] == None:
        status = "START"
    else:
        status = data['status']

    if data['notepad'] == None:
        notepad = dict()
    else:
        notepad = data['notepad'].json


    try:
        notepad['functions'] = "parking_recommendation, event_booking"
        notepad['user_requests'] = "- First I want to know where to park then I want to book a concert"
        output, status, notepad = identifyLogicalOperators(message, status, notepad, log) #add status when needed 
        # print(str(output))
        log("5")
        return jsonify(
            {
                'status': status,
                'notepad': notepad,
                'message': output, #status + "  " + 
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/demo", methods=["POST"])
def demo():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    log(data)
    if data["status"] == None:
        data["status"] = 0
    else:
        data["status"] = int(data["status"])

    if "message" not in data or not isinstance(data["message"], str):
        return jsonify({"error": "JSON must contain the 'message' key with a string value"}), 400

    if data["status"] == 0:
        response_message = "Your request is not valid.  I am afraid I cannot help you. Please ask me requests falling under the categories of the weather, ticket availability, event booking and parking recommendation"
        data["status"] += 1
    elif data["status"] == 1:
        response_message = "If I understand correctly, you want information about the weather and about parking recommendation. Is this correct?"
        data["status"] += 1
    elif data["status"] == 2:
        response_message = "I am sorry, I understood it wrong. you want information about the weather and about ticket availability. Is this correct?"
        data["status"] += 1 
    elif data["status"] == 3:
        response_message = "If I understand correctly, you want first to know about the weather and then about the ticket availability?"
        data["status"] += 1
    elif data["status"] == 4:
        response_message = "I am sorry, I understood it wrong. You want to know first about the ticket availability and then the weather?"
        data["status"] += 1
    else:
        response_message = "seq ['ticket_availability'; 'weather_checking']"
    

    return jsonify({"message": response_message,
                    "status" : str(data["status"])})

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
