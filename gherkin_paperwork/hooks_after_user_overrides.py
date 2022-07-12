import os

###############################################################################

def hooks_after_user_overrides(worker):
    print("## Hooks after user overrides\n")
    disable_doxygen_latex_if_option_disabled(worker)
    print("\n")

###############################################################################

def disable_doxygen_latex_if_option_disabled(worker):
    print(" - Disable doxygen latex generation if the option doxygen/output_latex is False")
    if worker.opts.doxygen["output_latex"] == False:
        worker.opts.doxyfile["GENERATE_LATEX"]          = "NO"
        worker.opts.doxyfile["USE_PDFLATEX"]            = "NO"

###############################################################################
