import sys 
import os 
from utils.process_repo import process_repo
from agents.planning_agent import PlanningAgent
from agents.builder_agent import BuildingAgent
import argparse 

# accept a src folder that it can point to
# if doesn't exist, create it 
# if exists, read it and process_existing over it 

if __name__ == "__main__":
    # get the src folder

    parser = argparse.ArgumentParser(
                    prog='AutoCode',
                    description='Generate code from an AutoGPT')

    parser.add_argument('-s', '--src')      # option that takes a value
    parser.add_argument('-t', '--task')      # option that takes a value

    args = parser.parse_args()

    src_folder = args.src
    task = args.task

    # multiple arg flags. --src <src_folder> --task project task 

    # gather requirements 
    project_type = "Next13"

    # check if it exists
    if not os.path.exists(src_folder):
        # if not, create it
        print("Initializing folder ", src_folder, "...")
        os.mkdir(src_folder)
    else:
        # if it does, process it
        process_repo(src_folder)

    # needs: what type of project is it? (gather from user)

    planner = PlanningAgent()
    description, steps = planner.execute(task, project_type)
    builder = BuildingAgent()
    for step in steps:
        builder.execute(step, description)

    # At each task:
    # provide file structure
    # actions:
    # - create file 
    # - edit file 
    # - delete file
    # - run tsc 
    # - run npm install <package> 
    # - look up file contents  
    # - look up docs / something on the internet (later) 