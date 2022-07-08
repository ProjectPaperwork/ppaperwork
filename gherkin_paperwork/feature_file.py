"""Represent Gherkin feature file as dataclasses

 Florian Dupeyron
 May 2022
"""

from dataclasses    import dataclass, field
import logging
from typing         import List
from textwrap       import dedent

from pathlib        import Path
from gherkin.parser import Parser

# ┌────────────────────────────────────────┐
# │ Generic dataclasses                    │
# └────────────────────────────────────────┘

@dataclass
class Location:
    column: int
    line: int


@dataclass
class Tag:
    id: int
    location: Location
    name: str

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["location"]

        location = Location(**data["location"])
        return cls(**dd2, location=location)




# ┌────────────────────────────────────────┐
# │ Data table                             │
# └────────────────────────────────────────┘

@dataclass
class DataTable_Cell:
    location: Location
    value: any

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["location"]

        return cls(**dd2,
            location = Location(**data["location"])
        )

@dataclass
class DataTable_Row:
    id: int
    location: Location
    cells: List[DataTable_Cell]

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["location"]
        del dd2["cells"   ]

        return cls(**dd2,
            location = Location(**data["location"]),
            cells    = [DataTable_Cell.from_dict(x) for x in data["cells"]]
        )

    def simplify(self):
        """
        Helper function that iterates through the row data
        """

        return (map(lambda x: x.value, self.cells))

@dataclass
class DataTable:
    location: Location
    rows: List[DataTable_Row]

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["location"]
        del dd2["rows"    ]

        return cls(**dd2,
            location = Location(**data["location"]),
            rows     = [DataTable_Row.from_dict(x) for x in data["rows"]]
        )

    def simplify(self):
        """
        Helper function that returns the table data as tuples.
        """

        return tuple(map(lambda x: x.simplify(), self.rows))


# ┌────────────────────────────────────────┐
# │ Examples for scenario outline          │
# └────────────────────────────────────────┘

@dataclass
class Example:
    id: int
    keyword: str
    location: Location
    name: str
    description: str
    tags:  List[Tag]
    tableHeader: List[DataTable_Row]
    tableBody: List[DataTable_Row]

    @classmethod
    def from_dict(cls, data):
        dd2 = data.copy()
        del dd2["location"   ]
        del dd2["tags"       ]
        del dd2["tableHeader"]
        del dd2["tableBody"  ]

        return cls(**dd2,
            location    = Location(**data["location"]),
            tags        = [Tag.from_dict(tag_desc) for tag_desc in data["tags"]],
            tableHeader = DataTable_Row.from_dict(data["tableHeader"]),
            tableBody   = [DataTable_Row.from_dict(row_desc) for row_desc in data["tableBody"]]
        )


# ┌────────────────────────────────────────┐
# │ Steps                                  │
# └────────────────────────────────────────┘

@dataclass
class Step:
    id: int
    keyword: str
    location: Location
    text: str
    dataTable: List[any] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        # Copy data, parse location
        dd2 = data.copy()
        del dd2["location"]
        del dd2["keywordType"]

        location  = Location(**data["location"])
        dataTable = None

        if "dataTable" in data:
            del dd2["dataTable"]
            dataTable = DataTable.from_dict(data["dataTable"])

        return cls(**dd2,
            location  = location,
            dataTable = dataTable
        )


# ┌────────────────────────────────────────┐
# │ Scenario                               │
# └────────────────────────────────────────┘

@dataclass
class Scenario:
    id: int
    keyword: str
    location: Location
    name: str
    description: str
    examples: List[Example]
    steps: List[Step]
    tags: List[str]

    @classmethod
    def from_dict(cls, data: dict):
        # Copy data and remove processed fields
        dd2   = data.copy()
        del dd2["description"]
        del dd2["steps"   ]
        del dd2["location"]
        del dd2["tags"    ]
        del dd2["examples"]

        # Process specific data fields
        location = Location(**data["location"])
        steps    = [Step.from_dict(step_desc) for step_desc in data["steps"]]
        tags     = [Tag.from_dict(tag_desc)   for tag_desc  in data["tags" ]]

        # Create Scenario object
        return cls(**dd2,
            description = dedent(data["description"]),
            location    = location,
            steps       = steps,
            tags        = tags,
            examples    = [Example.from_dict(example_desc) for example_desc in data["examples"]]
        )

# ┌────────────────────────────────────────┐
# │ Rule                                   │
# └────────────────────────────────────────┘

@dataclass
class Rule:
    id: int
    keyword: str
    location: Location
    name: str
    description: str
    tags: List[str]
    children: List[any]

    @classmethod
    def from_dict(cls, data: dict):

        # Copy data and remove processed fields
        dd2   = data.copy()
        del dd2["description"]
        del dd2["location"]
        del dd2["tags"    ]
        del dd2["children"]

        # Process tags and location
        location = Location(**data["location"])
        tags     = [Tag.from_dict(tag_desc) for tag_desc in data["tags"]]

        # print(data)

        # Process children
        def __process_child(c):
            if "scenario" in c:
                return Scenario.from_dict(c["scenario"])
            elif "rule" in c:
                return Rule.from_dict(c["rule"])
            elif "background" in c:
                return Background.from_dict(c["background"])

        children = [__process_child(c) for c in data["children"]]


        # Return final item
        return cls(**dd2,
            location    = location,
            description = dedent(data["description"]),
            tags        = tags,
            children    = children
        )



# ┌────────────────────────────────────────┐
# │ Background                             │
# └────────────────────────────────────────┘

@dataclass
class Background:
    id: int
    keyword: str
    location: Location
    name: str
    description: str
    steps: List[Step]

    @classmethod
    def from_dict(cls, data: dict):
        dd2 = data.copy()
        del dd2["location"]
        del dd2["steps"   ]

        location = Location(**data["location"])
        steps    = [Step.from_dict(step_desc) for step_desc in data["steps"]]
        
        return cls(**dd2,
            location = location,
            steps    = steps
        )


# ┌────────────────────────────────────────┐
# │ Feature                                │
# └────────────────────────────────────────┘

@dataclass
class Feature:
    keyword: str
    location: Location
    name: str
    description: str
    language: str
    tags: List[Tag]

    children: List[any]

    @classmethod
    def from_dict(cls, data):
        # Copy data and remove processed fields
        dd2 = data.copy()
        del dd2["children"   ]
        del dd2["description"]
        del dd2["location"   ]
        del dd2["tags"       ]

        # Process tags and location
        location = Location(**data["location"])
        tags     = [Tag.from_dict(tag_desc) for tag_desc in data["tags"]]

        # Process children
        def __process_child(c):
            if "scenario" in c:
                return Scenario.from_dict(c["scenario"])
            elif "rule" in c:
                return Rule.from_dict(c["rule"])
            elif "background" in c:
                return Background.from_dict(c["background"])

        children = [__process_child(c) for c in data["children"]]

        # Return final item
        return cls(**dd2,
            location    = location,
            description = dedent(data["description"]),
            tags        = tags,
            children    = children
        )


# ┌────────────────────────────────────────┐
# │ Helpers                                │
# └────────────────────────────────────────┘

def from_file(fpath: Path):
    fpath = Path(fpath)
    return Feature.from_dict(Parser().parse(str(fpath))["feature"])
