from argparse import ArgumentParser

from better_profanity import profanity
from detoxify import Detoxify
from flask import Flask, jsonify, request
from openai import OpenAI

from constants import BAD_INPUT_MESSAGE, BAD_OUTPUT_MESSAGE, NUMBER_OUTPUT_GENERATION, TOXICITY_THRESHOLD

app = Flask(__name__)


def set_llm_client(api_key, api_base):
    app.config["llm_client"] = OpenAI(
        api_key=api_key,
        base_url=api_base,
    )


def set_model_name(model_name):
    app.config["model_name"] = model_name


def get_model_name():
    """Return the model name."""
    return app.config.get("model_name")


def get_llm_client():
    """Return the LLM client using OpenAI."""
    return app.config.get("llm_client")


def set_toxify_model():
    app.config["toxify_model"] = Detoxify("unbiased", device="cuda")


def get_toxify_model():
    """Initialize and return the Detoxify model."""
    return app.config.get("toxify_model")


def is_bad_content(text):
    """Check if the input text contains profanity."""
    return profanity.contains_profanity(text)


def preprocess_input(input_text):
    """Preprocess user input by stripping whitespace."""
    return input_text.strip()


def generate_response(text):
    """Generate a JSON response with the given text."""
    return jsonify({"response": text})


def get_llm_output(llm_client, preprocessed_input, model_name):
    """Get the output from the LLM model for the preprocessed input."""
    response = llm_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": preprocessed_input}],
    )
    output_text = response.choices[0].message.content
    return output_text


def is_output_bad(output_text):
    """Check if the generated output contains profanity or high toxicity."""
    if profanity.contains_profanity(output_text):
        return True

    toxify_model = get_toxify_model()
    prediction = toxify_model.predict(output_text)

    if prediction["toxicity"] > TOXICITY_THRESHOLD:
        return True
    return False


@app.route("/process", methods=["POST"])
def process_request():
    """Process the incoming request and generate a response."""
    data = request.json
    user_input = data.get("input", "")

    # Check if input contains profanity
    if is_bad_content(user_input):
        return generate_response(BAD_INPUT_MESSAGE)

    # Preprocess the input
    preprocessed_input = preprocess_input(user_input)
    llm_client = get_llm_client()
    model_name = get_model_name()
    try:
        # Generate and check multiple outputs
        for _ in range(NUMBER_OUTPUT_GENERATION):
            output_text = get_llm_output(llm_client, preprocessed_input, model_name)

            if not is_output_bad(output_text):
                return generate_response(output_text)

        # Return message if all generated outputs are bad
        return generate_response(BAD_OUTPUT_MESSAGE)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--api-key", type=str, default="token-abc123", help="API key for OpenAI.")
    parser.add_argument(
        "--api-base", type=str, default="http://localhost:8000/v1/", help="Base URL for the OpenAI API."
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="meta-llama/Meta-Llama-3.1-8B-Instruct",
        help="Model name to use for completions.",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for Flask app.")
    parser.add_argument("--port", type=int, default=5000, help="Port for Flask app.")

    args = parser.parse_args()

    set_llm_client(args.api_key, args.api_base)
    set_toxify_model()
    set_model_name(args.model_name)

    app.run(host=args.host, port=args.port)
