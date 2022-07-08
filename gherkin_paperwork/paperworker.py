import os
import yaml
import shutil
import subprocess
from dataclasses    import dataclass, field
from typing         import List
from textwrap       import dedent

from io                             import (StringIO)
from tabulate                       import tabulate

from gherkin_paperwork.gherkin_dir_to_markdown_file import gherkin_dir_to_markdown_file
from gherkin_paperwork.options                      import Options

def directory_find(atom, root='.'):
    for path, dirs, files in os.walk(root):
        if atom in dirs:
            return os.path.join(path, atom)

def print_cmds(cmd_array):
    cmd_str = ""
    for part in cmd_array:
        cmd_str+= f"{part} "
    print(cmd_str)

class Paperworker:
    """Convert a features directory into a markdown file
    """

    ###########################################################################
    ###########################################################################

    def __init__(self) -> None:
        """Constructor
        """
        self.opts = Options()
        self.workDir = os.getcwd()
        self.paperworkFile = os.path.join(self.workDir, "gpaperwork.yml")

    ###########################################################################
    ###########################################################################

    def updateOptionsFromWorkingDirAnalysis(self):
        """
        """
        # Get project name from the readme
        try:
            with open('README.md') as f:
                first_line = f.readline()
                if first_line.startswith('#'):
                    first_line = first_line[1:]
                    first_line = first_line[:-1] # \n
                self.opts.doxyfile["PROJECT_NAME"] = first_line
        except:
            print("No 'README.md' file found to extract the name")

        # Update doxygen input from root directory
        dox_inputs=""
        for element in os.listdir(self.workDir):
            if element != "setup.py":
                dox_inputs+=f" {element}"
        self.opts.doxyfile["INPUT"] = dox_inputs
        
        #
        self.opts.gherkin["features_dir"] = directory_find("features")

    ###########################################################################
    ###########################################################################

    def parseUserOverrides(self):
        """
        """
        # Check if the paperwork file is here
        if not os.path.isfile(self.paperworkFile):
            print(f"No user overrides '{self.paperworkFile}'")
            return 

        # Parse file
        user_overrides=None
        with open(self.paperworkFile) as file:
            user_overrides = yaml.load(file, Loader=yaml.FullLoader)
        print(user_overrides)
        
        # Update options
        self.opts.jobs.update(user_overrides["jobs"])
        self.opts.common.update(user_overrides["doxygen"])
        self.opts.gherkin.update(user_overrides["gherkin"])
        self.opts.doxygen.update(user_overrides["doxygen"])
        self.opts.doxyfile.update(user_overrides["doxyfile"])


    ###########################################################################
    ###########################################################################

    def adaptSubOptions(self):
        """Check high level options to configure low level options
        """

        # 
        if self.opts.doxygen["include_gherkin"]:
            input_str = self.opts.doxyfile["INPUT"]
            input_str += f' {self.opts.common["output_directory"]}/gherkin/md_file'
           
    ###########################################################################
    ###########################################################################

    def work(self):
        """Main working function
        """
        print(f"Gherkin Paperwork !")

        #
        self.updateOptionsFromWorkingDirAnalysis()

        #
        self.parseUserOverrides()

        #
        self.adaptSubOptions()

        # Print job configuration
        print(f"=================================================")
        print(f"=================================================")
        print("OPTIONS")
        print("you can override using 'gpaperwork.yml'")
        print(yaml.dump(self.opts, default_flow_style=False))
        print(f"=================================================")
        print(f"=================================================")

        
        # Delete ouput if already exist
        if os.path.isdir(self.opts.common["output_directory"]):
            print(f"delete directory '{self.opts.common['output_directory']}'")
            shutil.rmtree(self.opts.common["output_directory"])
        os.makedirs(self.opts.common["output_directory"])

        #
        self.gherkin()
        self.doxygen()

    ###########################################################################
    ###########################################################################

    def gherkin(self):
        """Run the gherkin job
        """
        print(f"=================================================")
        print(f"=================================================")
        if not self.opts.jobs["gherkin"]:
            print(f"JOB: Gherkin => disabled")
            return
        print(f"JOB: Gherkin")

        # markdown file
        gherkin_dir_to_markdown_file(self.opts.gherkin["features_dir"], self.opts.common["output_directory"] + '/gherkin/md_file/features.md')

        # html
        os.makedirs( self.opts.common["output_directory"] + '/gherkin/html', exist_ok=True )
        cmds = [ "pandoc", "-s", "-o", self.opts.common["output_directory"] + '/gherkin/html/feature.html', self.opts.common["output_directory"] + '/gherkin/md_file/features.md' ]
        print_cmds(cmds)
        subprocess.run(cmds)
        
        # docx
        os.makedirs( self.opts.common["output_directory"] + '/gherkin/docx', exist_ok=True )
        cmds = [ "pandoc", "-s", "-o", self.opts.common["output_directory"] + '/gherkin/docx/feature.docx', self.opts.common["output_directory"] + '/gherkin/md_file/features.md' ]
        print_cmds(cmds)
        subprocess.run(cmds)
        

    ###########################################################################
    ###########################################################################

    def doxygen(self):
        """Run the doxygen job
        """
        print(f"=================================================")
        print(f"=================================================")
        if not self.opts.jobs["doxygen"]:
            print(f"JOB: Doxygen => disabled")
            return
        print(f"JOB: Doxygen")
        
        # Create the doxyfile
        f = open("Doxyfile", "w")
        for opt in self.opts.doxyfile:
            f.write(f"{opt} = {self.opts.doxyfile[opt]}\r\n")
        f.close()
        
        # Create the output directory if not exist
        if not os.path.isdir(self.opts.doxyfile["OUTPUT_DIRECTORY"]):
            os.makedirs( self.opts.doxyfile["OUTPUT_DIRECTORY"], exist_ok=True )
        
        # Run doxygen
        subprocess.run("doxygen", shell=True, check=True)

        # Cleanup
        os.remove("Doxyfile")

        # Check if the user wants the doxygen generation
        if self.opts.doxygen["output_pdf"]:
            # Generate the pdf
            latex_path = self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/' + 'latex'
            print(f"=================================================")
            print(f"=================================================")
            print(f"Doxygen PDF into {latex_path}")
            subprocess.run([ "make" ], shell=True, check=True, cwd=latex_path)
            
            # Copy the pdf at the right place
            os.makedirs( self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/pdf', exist_ok=True )
            shutil.copyfile(self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/latex/refman.pdf', self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/pdf/manual.pdf')

 
    ###########################################################################
    ###########################################################################

