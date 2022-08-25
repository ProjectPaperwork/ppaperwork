"""Simple conversion to markdown 

 This module uses the NodeVisitor mechanism to output markdown content
 to some given file.

 Uses tabulate to output tables using the grid format.

 Florian Dupeyron
 May 2022
"""

from gherkin_paperwork.node_visitor import NodeVisitor
from gherkin_paperwork.feature_file import (
    Scenario,
    Background,
    Feature,
    Step,
    Example
)
from tabulate                       import tabulate

class Markdown_NodeVisitor(NodeVisitor):
    def __init__(self, io):
        super().__init__()
        self.io = io

    # ┌────────────────────────────────────────┐
    # │ Process nodes stuff                    │
    # └────────────────────────────────────────┘
    
    def _process_feature(self, ft: Feature, **kwargs):
        print(f"## {ft.name}", file=self.io)

        if ft.description:
            print("", file=self.io)
            print(ft.description, file=self.io)


    def _process_rule(self, rule: Step, **kwargs):
        print("", file=self.io)
        print(f"### {rule.name}", file=self.io)
        
        if rule.description:
            print("", file=self.io)
            print(rule.description, file=self.io)


    def _process_scenario(self, sc: Scenario, **kwargs):
        print("", file=self.io)
        print(f"#### {sc.keyword.strip()}: {sc.name}", file=self.io)
        if sc.description:
            print("", file=self.io)
            print(sc.description, file=self.io)
        print("", file=self.io)
        print("_Procedure_: ", file=self.io)
        print("", file=self.io)


    def _process_background(self, bg: Background, **kwargs):
        print("", file=self.io)
        print(f"#### _{bg.keyword.strip()}_: {bg.name}", file=self.io)
        if bg.description:
            print("", file=self.io)
            print(bg.description, file=self.io)
        print("", file=self.io)
        print("_Checklist_:", file=self.io)
        print("", file=self.io)


    def _process_step(self, st: Step, **kwargs):
        # Process step text
        st_text = st.text.replace("<", "`<").replace(">", ">`")

        # Print step text
        if st.keyword in ("*", *kwargs["dialect"].and_keywords):
            print(f"- _{kwargs['dialect'].and_keywords[1].replace(' ','')}_ {st_text}", file=self.io)
        else:
            print(f"- _{st.keyword.strip()}_ {st_text}", file=self.io)

        # Print step datatable
        if st.dataTable:
            print("", file=self.io)
            data = st.dataTable.simplify()
            print(tabulate(data, tablefmt="grid"), file=self.io)
            print("", file=self.io)

    def _process_example(self, ex: Example, **kwargs):
        print("", file=self.io)
        print(f"##### _{ex.keyword}_: {ex.name}", file=self.io)
        if ex.description:
            print("", file=self.io)
            print(ex.description, file=self.io)
        print("", file=self.io)
        print(tabulate(
            tuple(map(lambda x: x.simplify(), ex.tableBody)),
            ex.tableHeader.simplify(),
            tablefmt="grid"
        ), file=self.io)
