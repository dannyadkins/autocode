import os

def initialize_project(src_folder):
    # check if it exists
    if not os.path.exists(src_folder):
        # if not, create it
        print("Initializing folder ", src_folder, "...")
        os.mkdir(src_folder)
