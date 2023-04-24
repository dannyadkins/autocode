import gpt4

class PlanningAgent:
    def __init__(self):
        pass 

    def execute(self, task, project_type):
        prompt = """You are an agent that is here to help the user create a codebase. 
        
        Your job is to plan out, in detail, each of the steps that other agents will take to create the codebase.

        Here is your task: {}

        You are working on a {} project.

        Please output the steps in a numbered list, with no other commentary. Consider all of the important steps that need to be taken to create the codebase and deploy it to production at scale.

        You may do the following:
        - run scripts to set up the repository 
        - plan features to build, with context about how they should fit in with other preexisting features
        - be extremely specific about what should be done where 

        DO NOT DO THE FOLLOWING:
        - do not delegate high-level design tasks, like setting up things on the Internet or "setting up the server"
        - do not be unspecific 
        - do not do anything that cannot be done on the frontend repository or directly in the codebase, such as dealing with a database or deploying to production
        - do not say to do things that aren't directly doable with code (e.g. "monitor the server"). Remember, you are talking to other code-based agents, not humans. 

        Please also describe the task at a high-level description with details that other agents can reference to understand what you are doing. Don't come up with any new ideas outside of the task; specifically explain the planned anatomy of the project and any high-level architectural decisions.

        Your output should look like: 
        DESCRIPTION 
        some description here 

        STEPS 
        1. some step
        2. some other step
        """
        prompt = prompt.format(task, project_type)

        print("Planner agent generating tasks...")
        completion = gpt4.get_completion(prompt)
        print(completion)
        description = completion.split("DESCRIPTION")[1].split("STEPS")[0].strip()
        steps = completion.split("STEPS")[1].split('\n')[1:]
        return description, steps




