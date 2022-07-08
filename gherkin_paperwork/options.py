import os
import yaml

class Options:
    """Contains options of the worker
    """
    
    ###########################################################################
    ###########################################################################

    def updateFromYml(self, ymlfilepath):
        # Check if the paperwork file is here
        if not os.path.isfile(ymlfilepath):
            print(f"No user overrides '{ymlfilepath}'")
            return 

        # Parse file
        user_overrides=None
        with open(ymlfilepath) as file:
            user_overrides = yaml.load(file, Loader=yaml.FullLoader)
        print(user_overrides)
        
        # Update options
        self.jobs.update(user_overrides["jobs"])
        self.common.update(user_overrides["doxygen"])
        self.gherkin.update(user_overrides["gherkin"])
        self.doxygen.update(user_overrides["doxygen"])
        self.doxyfile.update(user_overrides["doxyfile"])
    
    ###########################################################################
    ###########################################################################
    
    def __init__(self) -> None:
        
        #######################################################################
        # JOBS
        self.jobs = dict()
        self.jobs["gherkin"]=True
        self.jobs["doxygen"]=True

        #######################################################################
        # COMMON
        self.common = dict()
        self.common["output_directory"]="documentation"

        #######################################################################
        # GHERKIN
        self.gherkin = dict()
        self.gherkin["features_dir"]=None

        #######################################################################
        # DOXYGEN
        self.doxygen = dict()
        self.doxygen["output_html"]=True
        self.doxygen["output_latex"]=True
        self.doxygen["output_pdf"]=True
        self.doxygen["include_gherkin"]=True
        self.doxygen["ignore_path"]=['setup.py']

        #######################################################################
        # DOXYFILE
        self.doxyfile = dict()
        self.doxyfile["DOXYFILE_ENCODING"]       = "UTF-8"
        self.doxyfile["PROJECT_NAME"]            = "NAMELESS"
        self.doxyfile["PROJECT_LOGO"]            = "img/project_logo.svg"
        self.doxyfile["OUTPUT_DIRECTORY"]        = "documentation/doxygen"
        self.doxyfile["CREATE_SUBDIRS"]          = "YES"
        self.doxyfile["ALLOW_UNICODE_NAMES"]     = "NO"
        self.doxyfile["OUTPUT_LANGUAGE"]         = "English"
        self.doxyfile["HTML_EXTRA_STYLESHEET"]   = "/doxygen-awesome-css/doxygen-awesome.css"
        self.doxyfile["MARKDOWN_SUPPORT"]        = "YES"
        self.doxyfile["USE_MDFILE_AS_MAINPAGE"]  = "README.md"
        self.doxyfile["IMAGE_PATH"]              = "img"
        self.doxyfile["GENERATE_LATEX"]          = "YES"
        self.doxyfile["INPUT"]                   = "."
        self.doxyfile["RECURSIVE"]               = "YES"
        self.doxyfile["GENERATE_TREEVIEW"]       = "YES"
        self.doxyfile["EXCLUDE_PATTERNS"]        = "*/features/*"


        
