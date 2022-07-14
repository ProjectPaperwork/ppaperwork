import os
from fnmatch import fnmatch

###############################################################################

def hooks_after_user_overrides(worker):
    print("## Hooks after user overrides\n")
    disable_doxygen_latex_if_option_disabled(worker)
    fill_doxyfile_input_flag(worker)
    print("\n")

###############################################################################

def disable_doxygen_latex_if_option_disabled(worker):
    print(" - Disable doxygen latex generation if the option doxygen/output_latex is False")
    if worker.opts.doxygen["output_latex"] == False:
        worker.opts.doxyfile["GENERATE_LATEX"]          = "NO"
        worker.opts.doxyfile["USE_PDFLATEX"]            = "NO"

###############################################################################

# def fill_doxyfile_input_flag(worker):
#     print(" - Fill Doxygen INPUT with directories of the repository expect doxygen/ignore_path")
#     input_paths=""
#     for element in os.listdir(worker.workDir):
#         skip=False
#         for pattern in worker.opts.doxygen["ignore_path"]:
#             if fnmatch(element, pattern):
#                 print(f"        element ignored [{element}] / [{pattern}]")
#                 skip=True
#         if not skip:
#             input_paths+=f" {element}"            
#     worker.opts.doxyfile["INPUT"] = input_paths


def fill_doxyfile_input_flag(worker):
    print(" - Fill Doxygen INPUT with directories of the repository expect doxygen/ignore_path")
    input_paths=""
    
    for root, dirs, files in os.walk(worker.workDir):

        rel_root = root[len(worker.workDir)+1:]
        
        skip_root=False
        for pattern in worker.opts.doxygen["ignore_path"]:
            if fnmatch(rel_root, pattern):
                # print(f"        directory ignored [{rel_root}] / [{pattern}]")
                skip_root=True

        #
        if not skip_root:
            # print(rel_root)
            for file in files:                
                skip=False
                element = os.path.join(rel_root, file)
                for pattern in worker.opts.doxygen["ignore_path"]:
                    if fnmatch(element, pattern):
                        # print(f"        file ignored [{element}] / [{pattern}]")
                        skip=True
                if not skip:
                    input_paths+=f" {element}"
                
    worker.opts.doxyfile["INPUT"] = input_paths

###############################################################################

        