import openai
import json
from dotenv import load_dotenv
import os


class Mathdata:
    @staticmethod
    def get_stories(request):
        try:
            load_dotenv()
            openai.api_key = os.getenv('OPENAI_API_KEY')
            data = request.get_json(force=True)
            ccssCode = data["standard"]
            subject = data["subject"]

            # Creating a Json Template in which we require the output from ChatGPT
            json_template = """{
                "title": "title of the story",
                "story": "the story"
                }"""

            # Reading prompts from story_prompts.json file
            with open('new_story_prompt.json', 'r') as json_file:
                prompts_story = json.load(json_file)

            with open('story_schema.json', 'r') as json_file:
                story_template = json.load(json_file)
            
            user_input = f"{prompts_story[ccssCode].format(subject=subject)} Only return Json Object as output {json_template}"

            prompt = "You are a children's author and math interventionist who writes immersive, realistic narrative stories that embed mathematical concepts."

            # calling open AI for story generation
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
                temperature = 0.5,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input},
                ]
                # functions=[
                #     {"name": "get_stories", "parameters": story_template}
                # ]
            )

            message = response.choices[0].message.content
            print(message)
            message = message.replace("\n\n","\n")
            message = message.replace("  ","")
            story_data = json.loads(message, strict=False)

            return story_data
        except Exception as e:
            raise e

    @staticmethod
    def get_questions(request):
        try:
            load_dotenv()
            openai.api_key = os.getenv('OPENAI_API_KEY')
            data = request.get_json(force=True)
            ccssCode = data["standard"]
            subject = data["subject"]
            question = "3"
            if "question" in data:
                question = data["question"]
            story = False
            if "story" in data:
                story = data['story']
            print(data['story'])
            print(story)
            # Creating a definative Format in which we required Output from open AI
            with open('schema.json', 'r') as json_file:
                json_template = json.load(json_file)

            # Reading prompts from Questions_prompts.json file
            # with open('new_questions_prompt.json', 'r') as json_file:
            #     q_prompts = json.load(json_file)

            # prompt_q = q_prompts[ccssCode].format(subject=subject,question=question,json_template=json_template)
            
            # Calling the Chat GPT
            with open('questions_prompt.json', 'r') as json_file:
                prompt_q = json.load(json_file)
            user_input = prompt_q[ccssCode].format(story =story)
            print(user_input)
                # user_input = f"""{story}
                # Based on the story above, give me 3 word problems for  CCSS.{ccssCode}: se {description}  For example:"Taylor ate 11 ice cream bars over the summer. Grace ate 8 ice cream bars. How many more ice cream bars did Taylor eat than Grace? or "There are 5 bluebirds flying around. They found 9 more bluebirds. How many bluebirds are there altogether?" Make the questions multiple choice with 3 wrong answers based on common misconceptions for the math skill and one correct answer. Include all of the necessary information in each  word problem that the student needs to solve the problem. The three problems should be independent of one another.Provide a comprehensive explanation for why each of the four options is either right or wrong.Create hints that progressively guide students towards solving the problem. The first hint should introduce the concept, the second should provide an analogy, and the third should outline the step-by-step solution without revealing the answer."""
                # user_input =f"""
                # Perform the following tasks:
                # 1 Understand the Quantities and entities of this story: ```{story}```.
                # 2 Based on the context of the story above, give me {question} mathematical word problems for a {grade} grade aligned to the following stanard CCSS {ccssCode}: {description}.
                # 3 Provide all the quantities required to solve the mathematical problem with the questions. such that the questions can be solved without reading the story.
                # 4 Check the questions if they can be solved with the data in the question itself. Change the question if its not possible.
                # 5 Make the questions multiple choice with 4 distinct options and one correct answer.
                # 6 Provide a comprehensive explanation for why each of the four options is either right or wrong.
                # 7 Create hints that progressively guide students towards solving the problem. The first hint should introduce the concept, the second should provide an analogy, and the third should outline the step-by-step solution without revealing the answer. 
                # 8 Ensure accuracy: Verify that all mathematical explanations, hints, options, and answers are correct.
                # 9 Only return Json in the following format.
                # Json Format : '{json_template}'"""
                # user_input = f"""{story}
                # Only take the entity context from the story above and based on that give me 3 mathematical word problems for a {grade} grade aligned to the following standard CCSS {ccssCode}: {description}. Make sure that the question are only taking the reference from the story and the questions are testing mathematical skills.Make the questions multiple choice with 3 wrong answers based on common misconceptions for the math skill and one correct answer. Provide a comprehensive explanation for why each of the four options is either right or wrong.Create hints that progressively guide students towards solving the problem. The first hint should introduce the concept, the second should provide an analogy, and the third should outline the step-by-step solution without revealing the answer. Only return Json in the following format.
                # Json Format : '{json_template}'"""
            # else:
            #     prompt_q = q_prompts[ccssCode].format(subject=subject,question=question,json_template=json_template)
            #     user_input = f"""{prompt_q}"""
            # user_input = f"""{prompt_q} Only return a Json object with a 'data' array containing a Exactly 5 items. Each item includes a 'question' with 'option A', 'option B', 'option C' and 'option D' each having a 'value',an 'answer' (either True or False), and 'reasons'. It also includes 'hint1', 'hint2', and  'hint3' for hints related to the question. Additionally, there's a 'FunFact' field providing some fun facts. in the same json object outside the data array. do not give any comments. Remember the file is in a json format so enclosed all keys and values in double quote. Only return all the values specified in this json template {json_template}"""

            prompt = "Imagine you're a math teacher dedicated to creating effective math questions for students. Your goal is to craft meaningful multiple-choice math questions based on a given learning standard."

            response = openai.ChatCompletion.create(
                model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
                temperature = 0.5,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input},
                ],
                functions=[
                    {"name": "get_questions", "parameters": json_template}
                ]
            )

            # message = response.choices[0].message.content
            message = response.choices[0].message.function_call.arguments
            print(message)

            # making sure the data is in json
            if message[0] == '`':
                message = message.replace('```', "")
            questions_data = json.loads(message, strict=False)
            return questions_data

        except Exception as e:
            raise e

    @staticmethod
    def json_change(input_data):
        try:
            questions = input_data["data"]
            for question in questions:
                if "question" in question:
                    hints = []
                    for hint_num in range(1, 4):
                        hint_key = f"hint{hint_num}"
                        if hint_key in question:
                            hints.append(question[hint_key])
                            # Remove hint1, hint2, hint3 keys
                            del question[hint_key]
                    question["hints"] = hints
            return input_data
        except Exception as e:
            print(e)
            return input_data

    @staticmethod
    def funfacts(request):
        try:
            load_dotenv()
            openai.api_key = os.getenv('OPENAI_API_KEY')
            data = request.get_json(force=True)
            subject = data["subject"]
            prompt = "You are a Knowledeable Person who tells FunFacts with some though provoking questions"
            user_input = f"Give a fun fact related to the {subject} the fun fact should be interesting that can make student excited it should be kid friendly it should have a thought provoking question for the student. Do not start with ```Did you know```  the result should be not more that of 4 lines"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Change to "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input},
                ])
            message = response.choices[0].message.content
            return message

        except Exception as e:
            raise e