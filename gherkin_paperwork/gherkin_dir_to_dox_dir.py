import os
import shutil
import logging
import traceback

from gherkin.parser                 import Parser
from gherkin.dialect                import Dialect
from gherkin_paperwork.node_visitor import NodeVisitor
from gherkin_paperwork.markdown     import Markdown_NodeVisitor

from gherkin_paperwork.feature_file import (
    Feature,
    Scenario,
    Step,
    Example
)



def find_first_md_file_in_dir(dir):
    """Search in the directory to find a markdown file
    """
    for file in os.listdir(dir):
        if file.endswith(".md"):
            return os.path.join(dir, file)
    return None
            
            

def gherkin_dir_to_dox_dir(input_dir, output_dir):
    """
    """
    # Check input directory
    if input_dir == None:
        print(f"Input features directory is not provided : {input_dir}")
        return

    # Logs
    print(f"input_dir    : {input_dir}")
    print(f"output_dir   : {output_dir}")

    # Delete ouput if already exist
    if os.path.isdir(output_dir):
        print(f"delete directory '{output_dir}'")
        shutil.rmtree(output_dir)

    # Copy the entire input directory
    print(f"copy files from '{input_dir}' to '{output_dir}'")
    shutil.copytree(input_dir, output_dir) 

    # Embed the first '.md' file found in the features directory
    # readme_path=find_first_md_file_in_dir(output_dir)
    # if readme_path != None and os.path.isfile(readme_path):
    #     print(f"merge '{readme_path}' to '{output_file}'")
    #     shutil.copyfile(readme_path, output_file)
    #     print(f"remove '{readme_path}'")
    #     os.remove(readme_path)


    # Convert features
    for (dirpath, dirnames, filenames) in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.feature'):
                
                try:
                    # Get filename of the file to convert
                    file_path    = os.path.join(dirpath, filename)
                    print(f"Start converting '{file_path}'")
                    
                    # Get AST
                    feature_file = Parser().parse( os.path.join(dirpath, filename) )["feature"]
                    feature      = Feature.from_dict(feature_file)
                    
                    output_file  = filename.replace(".feature", ".md")
                    
                    # Convert into markdown
                    with open( output_file, "a" ) as fhandle:
                        nv = Markdown_NodeVisitor(fhandle)
                        nv.visit(feature)
                        fhandle.write("\n\n\n\n")

                    # Clean working file
                    os.remove(file_path)
                except:
                    print(f"fail converting '{file_path}'")
                    traceback.print_exc()


    
    print("")
