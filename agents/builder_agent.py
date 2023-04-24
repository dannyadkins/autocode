
from models import gpt4

class BuildingAgent:
    def __init__(self):
        pass 

    def execute(self, task, high_level_description):
        prompt = """You are an agent that is here to help the user create a codebase. 
        
        Your job is to build out pieces of code by editing files. 

        Here is your specific task, which comes from a broader: {}

        Here is the file structure of the project: 

        Please output the steps in a numbered list, with no other commentary. Consider all of the important steps that need to be taken to create the codebase and deploy it to production at scale.

        You may do the following actions:
        - CREATE <path>: creates a new file with the given path, relative to the root of the project
        - FETCH <path>: loads the contents of the file at the given path, relative to the root of the project
        - OVERWRITE <path> <contents>: overwrites the contents of the file at the given path, relative to the root of the project

        Please make sure you have all the information you might need. Consider which files you might need to edit, and what you might need to do to them.

        Your output should look like this, with no other commentary:
        STEPS
        1. some step
        2. some other step
        """
        prompt = prompt.format(task, high_level_description)

        print("Builder agent generating tasks...")
        print(gpt4.get_completion(prompt))



