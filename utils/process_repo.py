# extract from package.json, figure out the build script 

import json
import os
import sys

def process_repo(folder):
    # read the package.json file
    build_script, dev_script = get_package_scripts(folder)

def get_package_scripts(folder):
    build_script = None 
    dev_script = None 
    try: 
        with open(os.path.join(folder, "package.json")) as f:
            package = json.load(f)
        # extract the build script
        
    except Exception as e:
        print("Error: ", e)

    if (build_script):
        print("Build script: ", build_script)
    else: 
        print("No build script found")
    return build_script, dev_script