"""
┌──────────────────────────────────────────────┐
│ Helper class to process a parsed Gherkin AST │
└──────────────────────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

from gherkin_paperwork.feature_file import (
    Feature,
    Scenario,
    Background,
    Example,
    Rule,
    Step
)

from gherkin.dialect import Dialect

class NodeVisitor:
    """
    Helper class to process a parsed Gherkin AST.
    The User can inherit this class and implement
    the various visit and process functions to
    transform this tree in another formats
    (markdown, html, etc.).
    """

    # ┌────────────────────────────────────────┐
    # │ Public interface                       │
    # └────────────────────────────────────────┘

    def __init__(self):
        pass


    def visit(self, feature: Feature, **kwargs):
        return self._visit_feature(feature, **kwargs, dialect=Dialect.for_name(feature.language))


    # ┌────────────────────────────────────────┐
    # │ Process functions                      │
    # └────────────────────────────────────────┘
    
    def _process_feature(self, feature: Feature, **kwargs):
        pass

    def _process_scenario(self, sc: Scenario, **kwargs):
        pass
    
    def _process_background(self, bg: Background, **kwargs):
        pass

    def _process_example(self, ex: Example, **kwargs):
        pass

    def _process_step(self, st: Step, **kwargs):
        pass

    def _process_rule(self, rule: Step, **kwargs):
        pass


    # ┌────────────────────────────────────────┐
    # │ Visit functions                        │
    # └────────────────────────────────────────┘

    def _visit_feature(self, feature: Feature, **kwargs):
        self._process_feature(feature, **kwargs)
        for child in feature.children:
            if isinstance(child, Scenario):
                self._visit_scenario(child, **kwargs)
            elif isinstance(child, Rule):
                self._visit_rule(child, **kwargs)
            elif isinstance(child, Background):
                self._visit_background(child, **kwargs)


    def _visit_rule(self, rule: Rule, **kwargs):
        self._process_rule(rule, **kwargs)

        for child in rule.children:
            if isinstance(child, Scenario):
                self._visit_scenario(child, **kwargs)
            elif isinstance(child, Rule):
                self._visit_rule(child, **kwargs)
            elif isinstance(child, Background):
                self._visit_background(child, **kwargs)


    def _visit_scenario(self, sc: Scenario, **kwargs):
        self._process_scenario(sc, **kwargs)

        # Visit steps
        for step in sc.steps:
            self._visit_step(step, **kwargs)

        # Visit examples if any
        for examples in sc.examples:
            self._visit_examples(examples, **kwargs)

    def _visit_background(self, bg: Background, **kwargs):
        self._process_background(bg, **kwargs)

        # Visit steps
        for step in bg.steps:
            self._visit_step(step, **kwargs)


    def _visit_step(self, st: Step, **kwargs):
        self._process_step(st, **kwargs)


    def _visit_examples(self, ex: Example, **kwargs):
        self._process_example(ex, **kwargs)
