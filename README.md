# Project Paperwork

This repository regroups various experiments aiming at giving a simple way of generating
documentation from Gherkin_ files, using the canonical `gherkin-python`_ python module.

.. _Gherkin: https://cucumber.io/docs/gherkin/
.. _`gherkin-python`: https://github.com/cucumber/gherkin-python

Generate the example markdown file
==================================

1. Install the required dependencies:
    .. code:: bash

       pip install gherkin-official
       pip install tabulate

2. Execute the script!
    .. code:: bash
        
        python3 print_md_visitor.py

3. You can use pandoc to convert it to HTML:
    .. code:: bash
        
        pandoc -s -o output.html output.md


Scripts and signification
=========================

.. table::

    +-----------------------+-----------------------------------------------------------------------------------------+
    | Script name           | Role                                                                                    |
    +=======================+=========================================================================================+
    | `print_ast.py`        | Print the output AST from cucumber's gherkin parser                                     |
    +-----------------------+-----------------------------------------------------------------------------------------+
    | `print_steps.py`      | Print the restructured tree from `gherkin_paperwork`                                    |
    +-----------------------+-----------------------------------------------------------------------------------------+
    | `print_md.py`         | Simple script that takes that tree and prints markdown code                             |
    +-----------------------+-----------------------------------------------------------------------------------------+
    | `print_md_visitor.py` | Cleaner script using the `NodeVisitor` contraption to correctly print out markdown code |
    +-----------------------+-----------------------------------------------------------------------------------------+

