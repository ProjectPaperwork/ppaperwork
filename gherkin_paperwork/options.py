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
            print(f"**No user overrides ('ppaperwork.yml' on project root dir)**\n", flush=True)
            return

        # Parse file
        user_overrides=None
        with open(ymlfilepath) as file:
            user_overrides = yaml.load(file, Loader=yaml.FullLoader)
        
        # Update options
        if not user_overrides:
            print("**ERROR Parsing ppaperwork.yml**", flush=True)
        else:
            print(user_overrides)
            if "jobs" in user_overrides:
                self.jobs.update(user_overrides["jobs"])
            if "doxygen" in user_overrides:
                self.common.update(user_overrides["doxygen"])
            if "gherkin" in user_overrides:
                self.gherkin.update(user_overrides["gherkin"])
            if "doxygen" in user_overrides:
                self.doxygen.update(user_overrides["doxygen"])
            if "doxyfile" in user_overrides:
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
        self.gherkin["features_generated_md_filename"]='features_unified.md'

        #######################################################################
        # DOXYGEN
        self.doxygen = dict()
        self.doxygen["output_html"]=True
        self.doxygen["output_latex"]=False
        self.doxygen["include_gherkin"]=True
        self.doxygen["ignore_path"]=['setup.py', '.github/*', '.git/*', '.gitignore', 'documentation/*', '*/features/*']

        #######################################################################
        # DOXYFILE
        self.doxyfile = dict()
        self.doxyfile["DOXYFILE_ENCODING"]       = "UTF-8"
        self.doxyfile["PROJECT_NAME"]            = "NAMELESS"
        self.doxyfile["PROJECT_LOGO"]            = "img/project_logo.png"
        self.doxyfile["OUTPUT_DIRECTORY"]        = "documentation/doxygen"
        self.doxyfile["CREATE_SUBDIRS"]          = "YES"
        self.doxyfile["ALLOW_UNICODE_NAMES"]     = "YES"
        self.doxyfile["OUTPUT_LANGUAGE"]         = "English"
        self.doxyfile["HTML_EXTRA_STYLESHEET"]   = "/doxygen-awesome-css/doxygen-awesome.css"
        self.doxyfile["MARKDOWN_SUPPORT"]        = "YES"
        self.doxyfile["USE_MDFILE_AS_MAINPAGE"]  = "./README.md"
        self.doxyfile["IMAGE_PATH"]              = "img"
        self.doxyfile["GENERATE_LATEX"]          = "YES"
        self.doxyfile["USE_PDFLATEX"]            = "YES"
        self.doxyfile["INPUT"]                   = "."
        self.doxyfile["RECURSIVE"]               = "YES"
        self.doxyfile["GENERATE_TREEVIEW"]       = "YES"
        self.doxyfile["EXCLUDE_PATTERNS"]        = "*/features/*"
        self.doxyfile["EXTRACT_ALL"]             = "YES"

        
        