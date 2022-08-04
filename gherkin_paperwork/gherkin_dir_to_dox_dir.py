import os
import shutil
import logging

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



    
    print("")
