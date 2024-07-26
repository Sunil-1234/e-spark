from dotenv import load_dotenv
import os
from flask import jsonify
import requests

def load_offensive_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.read().split(',')]

def check_for_offensive_words(sentence, offensive_words):
    words = sentence.lower().split()
    for word in words:
        if word in offensive_words:
            return True
    return False

offensive_words = load_offensive_words('data/offensive_words.txt')

class Moderation:

    @staticmethod
    def analyze_text(request):
        try:
            load_dotenv()

            data = request.get_json(force=True)
            text_data = data["subject"]
            moderation_flag = data["moderationFlag"]

            if moderation_flag == 1:
                # If moderation_flag is equal to one then it means that the subject is added from text box
                if text_data is None:
                    raise ('Missing query parameter "text_data"')
                    # return jsonify({'error': 'Missing query parameter "text_data"'}), 400

                headers = {
                    'Authorization': os.getenv('HIVE_API_KEY'),
                }

                data = {
                    'text_data': text_data,
                    'metadata': '{"my_UUID": "3c78fc82-f797-11ea-adc1-0242ac120002"}'
                }

                response = requests.post('https://api.thehive.ai/api/v2/task/sync',
                                         headers=headers,
                                         data=data)

                response_dict = response.json()
                output_classes = response_dict['status'][0]['response']['output'][0]['classes']
                flag = 1 if any(class_info['score'] >
                                0 for class_info in output_classes) else 0
                if flag == 0:
                    is_offensive = check_for_offensive_words(text_data, offensive_words)
                    flag = 1 if is_offensive else 0

                # result = {
                #     'text': text_data,
                #     'flag': flag
                # }

                return flag

            else:
                # If moderation_flag is equal to one then it means that the subject is added from radio buttons
                return 0

        except Exception as e:
            raise e

# http://127.0.0.1:5000/analyze_text?text_data=

# from the open text, the string entered will pe passed as example: http://127.0.0.1:5000/analyze_text?text_data=nazi%20theme%20park
# if flag = 1, then it is offensive, hence the other open ai call will not be passed, and hence user has to enter the text again,
# then again for every text entered after submitting, the string will be passed to the api again like http://127.0.0.1:5000/analyze_text?text_data=theme%20park, this will return flag = 0, and hence the term is not offensive, and then the further api calls will be made.
