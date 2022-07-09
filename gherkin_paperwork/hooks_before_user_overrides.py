import os

###############################################################################

def hooks_before_user_overrides(worker):
    """
    """
    append_dir_with_image_to_doxyfile(worker)

###############################################################################

def append_dir_with_image_to_doxyfile(worker):
    """Doxygen needs to know where are the images to store them with html output
    """
    image_path=""
    for root, dirs, files in os.walk(worker.workDir):
        for dir in dirs:
            if dir == "img":
                dirpath = os.path.join(root, dir)
                dirpath = dirpath[len(worker.workDir)+1:]
                image_path += f" {dirpath}"
    worker.opts.doxyfile["IMAGE_PATH"] = image_path

###############################################################################
