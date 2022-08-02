from genericpath import isfile
import os
from fnmatch import fnmatch

###############################################################################

def hooks_before_user_overrides(worker):
    print("## Hooks before user overrides\n")
    append_dir_with_image_to_doxyfile(worker)
    propose_a_placeholder_for_the_project_logo(worker)
    print("\n")

###############################################################################

def append_dir_with_image_to_doxyfile(worker):
    print(" - Fill Doxygen IMAGE_PATH => needs to know where are the images to store them with html output")
    image_path=""
    for root, dirs, files in os.walk(worker.workDir):
        for dir in dirs:
            if dir == "img":
                dirpath = os.path.join(root, dir)
                dirpath = dirpath[len(worker.workDir)+1:]
                image_path += f" {dirpath}"
    worker.opts.doxyfile["IMAGE_PATH"] = image_path

###############################################################################

def propose_a_placeholder_for_the_project_logo(worker):
    print(" - Propose a placeholder for the project logo")
    if not os.path.isfile("img/project_logo.png"):
        worker.opts.doxyfile["PROJECT_LOGO"] = "/setup/project_logo.png"
        print("\t\tplaceholder used!")

###############################################################################

