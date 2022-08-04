import os
import sys
# import pytz
import yaml
import shutil
import subprocess
import time
from time import gmtime, strftime
from tzlocal import get_localzone

from datetime       import datetime
from dataclasses    import dataclass, field
from typing         import List
from textwrap       import dedent

from io                             import (StringIO)
from tabulate                       import tabulate

from gherkin_paperwork.options                      import Options

from gherkin_paperwork.gherkin_dir_to_dox_dir       import gherkin_dir_to_dox_dir
from gherkin_paperwork.gherkin_dir_to_markdown_file import gherkin_dir_to_markdown_file

from gherkin_paperwork.hooks_before_user_overrides  import hooks_before_user_overrides
from gherkin_paperwork.hooks_after_user_overrides   import hooks_after_user_overrides


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
        self.paperworkFile = os.path.join(self.workDir, "ppaperwork.yml")

    ###########################################################################
    ###########################################################################

    def subprocessLogFile(self, filename):
        """Build the path for the logs of subprocesses and create it if needed then return the path to the file
        """
        doxygen_log_dir=os.path.join(self.opts.common["output_directory"], 'logs')
        if not os.path.isdir(doxygen_log_dir):
            os.makedirs(doxygen_log_dir)
        return os.path.join(doxygen_log_dir, filename)

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


        #
        self.opts.gherkin["features_dir"] = directory_find("features")


    ###########################################################################
    ###########################################################################

    def adaptSubOptions(self):
        """Check high level options to configure low level options
        """

        # 
        if self.opts.doxygen["include_gherkin"]:
            self.opts.doxyfile["INPUT"] += f' {self.opts.common["output_directory"]}/gherkin/md_file'

        # Disable gherkin job if the features dir is not found or provided
        if not self.opts.gherkin["features_dir"]:
            print(f"gherkin.features_dir is not defined {self.opts.gherkin['features_dir']} => gherkin job is disabled")
            self.opts.jobs["gherkin"] = False

           
    ###########################################################################
    ###########################################################################

    def work(self):
        """Main working function
        """
        # Tz does not work yet
        d = datetime.now(tz=get_localzone())
        gen_datetime = d.strftime('%d/%m/%Y > %H:%M:%S')
        
        # Main title
        print(f"# Project Paperwork {gen_datetime}\n", flush=True)

        #
        hooks_before_user_overrides(self)

        #
        self.updateOptionsFromWorkingDirAnalysis()
        sys.stdout.flush()

        #
        self.opts.updateFromYml(self.paperworkFile)
        sys.stdout.flush()

        #
        hooks_after_user_overrides(self)
        self.adaptSubOptions()
        sys.stdout.flush()

        # Print job configuration
        print("## FILES IN WORKING DIRECTORY ${self.workDir}\n")
        arr = os.listdir(self.workDir)
        print(arr)
        print("\n")
        print("## OPTIONS\n")
        print("you can override using 'ppaperwork.yml'")
        print(yaml.dump(self.opts, default_flow_style=False))
        
        
        
        # Delete ouput if already exist
        if os.path.isdir(self.opts.common["output_directory"]):
            print(f"reset output directory '{self.opts.common['output_directory']}'")
            shutil.rmtree(self.opts.common["output_directory"])
        os.makedirs(self.opts.common["output_directory"])



        # Create a little readme for new users
        readme_filepath=os.path.join(self.opts.common["output_directory"], 'README.md')
        with open(readme_filepath, "w") as rdfile:
            rdfile.write(f'# Project Paperwork Documentation\n\n')
            rdfile.write(f'generation date time : {gen_datetime} \n\n')
            rdfile.write(f'This documentation has been generated with [ppaperwork](https://github.com/ProjectPaperwork/ppaperwork/pkgs/container/ppaperwork) \n\n')
            rdfile.write(f'# Open Doxygen Documentation\n\n')
            rdfile.write(f'To open the doxygen documentation doucle click on:\n\n')
            rdfile.write(f'- *doxygen-documentation.html*\n')
            rdfile.write(f'- *doxygen/html/index.html*\n')
            rdfile.write(f'\n')
            rdfile.write(f'your web browser should open and display the doxygen html documentation')
                
            
        #
        sys.stdout.flush()
        self.gherkin()
        self.doxygen()

    ###########################################################################
    ###########################################################################

    def gherkin(self):
        """Run the gherkin job
        """
        # Log
        print("## Gherkin Actions\n")
        if not self.opts.jobs["gherkin"]:
            print(f"!!! disabled !!!\n")
            return
    
        # Local variables
        generated_md_filepath = os.path.join(self.opts.common["output_directory"], 'gherkin', 'md_file', self.opts.gherkin["features_generated_md_filename"])
        generated_md_dirpath = os.path.join(self.opts.common["output_directory"], 'gherkin', 'md_dir')

        # markdown dir
        print("### Convert features into a directory for doxygen integration\n")
        gherkin_dir_to_dox_dir(self.opts.gherkin["features_dir"], generated_md_dirpath)

        # markdown file
        print("### Convert features into a unique markdown file\n")
        gherkin_dir_to_markdown_file(self.opts.gherkin["features_dir"], generated_md_filepath)

        # html
        os.makedirs( self.opts.common["output_directory"] + '/gherkin/html', exist_ok=True )
        cmds = [ "pandoc", "-s", "-o", self.opts.common["output_directory"] + '/gherkin/html/feature.html', generated_md_filepath ]
        print_cmds(cmds)
        subprocess.run(cmds)
        
        # docx
        os.makedirs( self.opts.common["output_directory"] + '/gherkin/docx', exist_ok=True )
        cmds = [ "pandoc", "-s", "-o", self.opts.common["output_directory"] + '/gherkin/docx/feature.docx', generated_md_filepath ]
        
        # 
        docx_templatepath = os.path.join( os.getcwd(), "file/template_docx.docx")
        if os.path.isfile(docx_templatepath):
            print(f"Docx template found ! {docx_templatepath}")
            cmds.append("--reference-doc")
            cmds.append(docx_templatepath)
        else:
            print("No docx template found !")
        print_cmds(cmds)
        subprocess.run(cmds)
        

    ###########################################################################
    ###########################################################################

    def doxygen(self):
        """Run the doxygen job
        """
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
        doxygen_log_file=self.subprocessLogFile('doxygen.txt')
        with open(doxygen_log_file, "w") as logfile:
            subprocess.run("doxygen", shell=True, check=True, stdout=logfile, stderr=logfile)

        # Create a link to redirect to inddex.html and ease user interaction
        doxygen_redir_file_path=os.path.join(self.opts.common["output_directory"], 'doxygen-documentation.html')
        with open(doxygen_redir_file_path, "w") as redirfile:
            redirfile.write('<meta http-equiv="refresh" content="0; URL=doxygen/html/index.html"/>')
        
        # Cleanup
        os.remove("Doxyfile")

        # # Check if the user wants the doxygen generation
        # if self.opts.doxygen["output_pdf"]:
        #     # Generate the pdf
        #     latex_path = self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/' + 'latex'
        #     print(f"=================================================")
        #     print(f"Doxygen PDF into {latex_path}")
        #     doxygen_log_file=self.subprocessLogFile('doxygen_latex_to_pdf.txt')
        #     try:
        #         with open(doxygen_log_file, "w") as logfile:
        #             subprocess.run([ "make" ], shell=True, check=True, cwd=latex_path, stdout=logfile, stderr=logfile)
            
        #         # Copy the pdf at the right place
        #         os.makedirs( self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/pdf', exist_ok=True )
        #         shutil.copyfile(self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/latex/refman.pdf', self.opts.doxyfile["OUTPUT_DIRECTORY"] + '/pdf/manual.pdf')
        #     except:
        #         print(f"DOXYGEN LATEX TO PDF FAILED (see {doxygen_log_file})")            
 
    ###########################################################################
    ###########################################################################

