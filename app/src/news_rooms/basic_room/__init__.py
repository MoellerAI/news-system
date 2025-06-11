\
# This file makes the basic_room directory a Python package.

from .basic_investigator_one import BasicInvestigatorOne
from .basic_investigator_two import BasicInvestigatorTwo
from .basic_editor import BasicEditor
from .basic_news_room import BasicNewsRoom

__all__: list[str] = [
    "BasicInvestigatorOne",
    "BasicInvestigatorTwo",
    "BasicEditor",
    "BasicNewsRoom",
]
