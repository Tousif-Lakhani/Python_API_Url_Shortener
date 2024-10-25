from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import string
import random
from datetime import datetime

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "URL-Shortner"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

url_map = {}


def generate_short_code():
    '''
    Generates a random short code.

    Returns:
        short_code (str): A randomly generated short code.
    '''
    characters = string.ascii_lowercase + string.digits + '_'
    short_code = ''

    for i in range(6):
        short_code += random.choice(characters)

    return short_code


def get_timestamp():
    """
    Get the current timestamp.

    Returns:
        str: Current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_shortcode(custom_code):
    '''
    Validate the custome shortcode.

    Parameter:
        custom_code (str): The shortcode to be validated.

    Returns:
        bool: True if the shortcode is valid or False otherwise.
    '''
    if len(custom_code) != 6:
        return False

    for char in custom_code:
        if not (char.isalnum() or char == "_"):
            return False

    return True


def create_short_url(original_url, custom_code=None):
    '''
    Create a short URL.

    Parameter:
        original_url (str): The original URL to be shortened.
        custom_code (str): Custom shortcode (optional).

    Returns:
        tuple: A tuple containing response data and status code.
    '''

    if not original_url:
        return jsonify({"error": "url not found"}), 400

    if custom_code:
        if not validate_shortcode(custom_code):
            return jsonify("The provided shortcode is invalid"), 412

        if custom_code in url_map:
            return jsonify("Shortcode already in use"), 409
    else:
        custom_code = generate_short_code()

    new_record = {
            custom_code: {
                'short_code': custom_code,
                'url': original_url,
                "created": get_timestamp(),
                "redirect_count": 0,
                "last_redirect": ""
                }
            }

    url_map.update(new_record)

    return jsonify({'shortcode': new_record[custom_code]["short_code"]}), 201


@app.route("/shorten", methods=["POST"])
def shorten_url():
    '''
    Shorten a URL.

    Returns:
        tuple: A tuple containing response data and status code.
    '''
    data = request.get_json()
    original_url = data['url']
    custom_code = data['shortcode']

    return create_short_url(original_url, custom_code)


@app.route('/<short_code>', methods=['Get'])
def extract_url(short_code):
    '''
    Extract the original URL from the short code.

    Parameter:
        shotr_code(str): The short code used to retrieve the original URL.

    Returns:
        tuple: A tuple containing the original URL with location header.
    '''

    if short_code in url_map:
        url_map[short_code]['redirect_count'] += 1
        url_map[short_code]['last_redirect'] = get_timestamp()
        return jsonify({"location": url_map[short_code]['url']}), 302
    else:
        return jsonify('Shortcode not found'), 404


@app.route('/<shortcode>/stats', methods=['GET'])
def get_statistics(shortcode):
    '''
    Get statistics for a specific short code.

    Parameter:
        shortcode(str): Short code for which statistics are requested.

    Returns:
        tuple: A tuple containing response data and status code.
    '''
    if shortcode in url_map:
        data = url_map[shortcode]
        return jsonify({
            "created": data['created'],
            "last_redirect": data["last_redirect"],
            "redirect_count": data["redirect_count"]
        }), 200
    else:
        return jsonify('Shortcode not found'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
