import base64
import replicate
import requests
import os
from dotenv import load_dotenv


class Image:

    @staticmethod
    def get_images(request):

        try:

            load_dotenv()

            data = request.get_json(force=True)

            subject = data["subject"]

            # Code to get image

            theme = subject
            print("calling Replicate for image generations ")
            output = replicate.run("stability-ai/sdxl:d830ba5dabf8090ec0db6c10fc862c6eb1c929e1a194a5411852d25fd954ac82",
                                   input={
                                       "prompt": f"A background of {theme} world showing the character, animated in pixar style, appropriate for a child"},
                                   height=540,
                                   width=960
                                   )

            # image moderation
            url = "https://api.thehive.ai/api/v2/task/sync"
            image_url = output[0]
            print(f"the image url is {image_url}")
            payload = {"url": image_url}

            headers = {
                "accept": "application/json",
                "authorization": "token YEBLGSQ7FVnZiGnjGwUo6qhqJyfcSnrO"
            }

            hive_response = requests.request(
                "POST", url, headers=headers, data=payload)
            json_data = hive_response.json()

            bad_classes = [
                "general_nsfw",
                "general_suggestive",
                "yes_female_underwear",
                "yes_male_underwear",
                "yes_sex_toy",
                "yes_female_nudity",
                "yes_male_nudity",
                "yes_female_swimwear",
                "yes_male_shirtless",
                "animated_gun",
                "gun_in_hand",
                "very_bloody",
                "yes_pills",
                "yes_smoking",
                "illicit_injectables",
                "medical_injectables",
                "yes_nazi",
                "yes_kkk",
                "yes_middle_finger",
                "yes_terrorist",
                "yes_sexual_activity",
                "hanging",
                "noose",
                "yes_realistic_nsfw",
                "animated_corpse",
                "human_corpse",
                "yes_self_harm",
                "yes_emaciated_body",
                "yes_sexual_intent",
                "animal_genitalia_and_human",
                "animal_genitalia_only",
                "animated_animal_genitalia",
                "yes_gambling",
                "yes_undressed",
                "yes_confederate",
                "animated_alcohol",
                "yes_alcohol",
                "yes_drinking_alcohol",
                "yes_religious_icon",
                "culinary_knife_in_hand",
                "knife_in_hand",
                "a_little_bloody",
                "other_blood"
            ]

            class_scores = json_data['status'][0]['response']['output'][0]['classes']
            class_scores_dict = {}

            for item in class_scores:
                class_name = item['class']
                score = item['score']
                if class_name in bad_classes:
                    class_scores_dict[class_name] = score

            flagged = any(
                score >= 0.95 for score in class_scores_dict.values())

            if (flagged == False):
                # response = requests.get(output[0])
                print(f"this is the response got {image_url}")
                # response.raise_for_status()  # Raise an exception if there's an error
                return image_url
            # # Convert the image content to base64
            # print("converting to base 64")
            # image_base64 = base64.b64encode(
            #     response.content).decode('utf-8')
            # print("the base 64 conversion is done")
            # End of image api function

            

        except Exception as e:

            raise e
