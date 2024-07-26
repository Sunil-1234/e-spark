
from flask import *
from flask_cors import CORS
from mathdata import Mathdata
from image import Image
from moderation import Moderation
from middleware import *

app = Flask(__name__)
CORS(app)


class Offensive_Word(Exception):
    pass


@app.route('/authentication', methods=["GET"])
def first_authentication():

    token = generate_jwt()

    return {"status_code": 200, "token": token}


@app.route('/get_image', methods=["POST"])
def get_image():
    if request.method == "POST":
        images = Image.get_images(request)
        # return {"status_code": 200, "imageurl": images["imgurl"], "image_data": images["base64"]}
        return {"status_code": 200, "image_data": images}


@app.route('/get_story', methods=["POST"])
@verify_decorator
def get_story(token_verify, *args, **kwargs):
    # def get_story():
    if request.method == "POST":
        text_moderation_result = Moderation.analyze_text(request)
        if text_moderation_result == 1:
            raise Offensive_Word(
                "Offensive word found!! Please enter another theme to continue")
        else:
            story_data = Mathdata.get_stories(request)
            return {"status_code": 200, "story_data": story_data}


@app.route('/get_questions', methods=["POST"])
@verify_decorator
def get_questoins(token_verify, *args, **kwargs):
    # def get_questions():
    if request.method == "POST":
        data = Mathdata.get_questions(request)
        data = Mathdata.json_change(data)
        return {"status_code": 200, "data": data}


@app.route('/get_fun_fact', methods=["POST"])
@verify_decorator
def get_facts(token_verify, *args, **kwargs):
    if request.method == "POST":
        data = Mathdata.funfacts(request)
        return {"status_code": 200, "data": data}


@app.route('/analyze_text', methods=["GET"])
def analyze_text():
    if request.method == "GET":
        result = Moderation.analyze_text(request)
        return {"status_code": 200, "flag": result}

# Exception handling function


@app.errorhandler(Exception)
def exception_handler(error):
    return {"data": "API Error", "error": str(error), "status_code": 500}, 500

# 404 error handling function


@app.errorhandler(404)
def not_found(error):
    return {"data": "404 error", "error": "Page Not Found!", "status_code": 404}, 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
