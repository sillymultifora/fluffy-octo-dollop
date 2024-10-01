from argparse import ArgumentParser
from better_profanity import profanity
from flask import Flask, jsonify, request, g
from openai import OpenAI
from detoxify import Detoxify
from constants import BAD_INPUT_MESSAGE, NUMBER_OUTPUT_GENERATION, TOXICITY_THRESHOLD, BAD_OUTPUT_MESSAGE

app = Flask(__name__)

# Global variables for API credentials and model name
openai_api_key = None
openai_api_base = None
model_name = None


def get_llm_client():
    if "llm_client" not in g:
        g.llm_client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
    return g.llm_client


def get_toxify_model():
    if "toxify_model" not in g:
        g.toxify_model = Detoxify("unbiased")
    return g.toxify_model


def is_bad_content(text):
    return profanity.contains_profanity(text)


def preprocess_input(input_text):
    return input_text.strip()


def postprocess_output(output_text):
    return output_text


def generate_response(text):
    return jsonify({"response": text})


def get_llm_output(llm_client, preprocessed_input):
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": preprocessed_input}],
    )
    output_text = response.choices[0].message.content
    return output_text


def is_output_bad(output_text):
    if profanity.contains_profanity(output_text):
        return True
    toxify_model = get_toxify_model()
    prediction = toxify_model.predict(output_text)
    print(prediction)
    if prediction["toxicity"] > TOXICITY_THRESHOLD:
        return True


@app.route("/process", methods=["POST"])
def process_request():
    data = request.json
    user_input = data.get("input", "")

    if is_bad_content(user_input):
        return generate_response(BAD_INPUT_MESSAGE)

    preprocessed_input = preprocess_input(user_input)
    llm_client = get_llm_client()
    try:
        for _ in range(NUMBER_OUTPUT_GENERATION):
            output_text = get_llm_output(llm_client, preprocessed_input)
            if not is_output_bad(output_text):
                postprocessed_output = postprocess_output(output_text)
                return generate_response(postprocessed_output)
        return generate_response(BAD_OUTPUT_MESSAGE)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--api-key", type=str, required=True, help="API key for OpenAI.")
    parser.add_argument("--api-base", type=str, required=True, help="Base URL for the OpenAI API.")
    parser.add_argument("--model-name", type=str, required=True, help="Model name to use for completions.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for Flask app.")
    parser.add_argument("--port", type=int, default=5000, help="Port for Flask app.")
    args = parser.parse_args()

    # Set global variables for API key, base URL, and model name
    openai_api_key = args.api_key
    openai_api_base = args.api_base
    model_name = args.model_name
    with app.app_context():
        get_llm_client()
        get_toxify_model()
    app.run(host=args.host, port=args.port)
