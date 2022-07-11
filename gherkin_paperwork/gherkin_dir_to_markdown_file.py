import os
import shutil
import logging
import traceback

from gherkin.dialect                import Dialect
from gherkin.parser                 import Parser

from gherkin_paperwork.node_visitor import NodeVisitor
from gherkin_paperwork.feature_file import (
    Feature,
    Scenario,
    Step,
    Example
)

from gherkin_paperwork.markdown     import Markdown_NodeVisitor


def find_first_md_file_in_dir(dir):
    """Search in the directory to find a markdown file
    """
    for file in os.listdir(dir):
        if file.endswith(".md"):
            return os.path.join(dir, file)
    return None
            
            

def gherkin_dir_to_markdown_file(input_dir, output_file):
    """Convert a gherkin features directory to a markdown file
    """
    # Extract data
    output_dir = os.path.dirname(output_file)

    # Check input directory
    if input_dir == None:
        logging.info(f"Input features directory is not provided : {input_dir}")
        return

    # Logs
    logging.info(f"input_dir    : {input_dir}")
    logging.info(f"output_dir   : {output_dir}")
    logging.info(f"output_file  : {output_file}")

    # Delete ouput if already exist
    if os.path.isdir(output_dir):
        logging.info(f"delete directory '{output_dir}'")
        shutil.rmtree(output_dir)

    # Copy the entire input directory
    logging.info(f"copy files from '{input_dir}' to '{output_dir}'")
    shutil.copytree(input_dir, output_dir) 

    # Embed the first '.md' file found in the features directory
    readme_path=find_first_md_file_in_dir(output_dir)
    if os.path.isfile(readme_path):
        logging.info(f"merge '{readme_path}' to '{output_file}'")
        shutil.copyfile(readme_path, output_file)
        logging.info(f"remove '{readme_path}'")
        os.remove(readme_path)

    # Convert features
    for (dirpath, dirnames, filenames) in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.feature'):
                
                try:
                    # Get filename of the file to convert
                    file_path    = os.path.join(dirpath, filename)
                    logging.info(f"Start converting '{file_path}'")
                    
                    # Get AST
                    feature_file = Parser().parse( os.path.join(dirpath, filename) )["feature"]
                    feature      = Feature.from_dict(feature_file)
                    
                    # Convert into markdown
                    with open( output_file, "a" ) as fhandle:
                        nv = Markdown_NodeVisitor(fhandle)
                        nv.visit(feature)
                        fhandle.write("\n\n\n\n")

                    # Clean working file
                    os.remove(file_path)
                except:
                    logging.error(f"fail converting '{file_path}'")
                    traceback.print_exc()


