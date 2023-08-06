# pylint: disable=inherit-non-class
from typing import List, Union, Dict, TypedDict, Optional
from enum import Enum


class OpenContext(Enum):
    BROWSE = "Browse"
    QUICK_LAUNCH = "QuickLaunch"


DirectorySchema = List[Union[str, Dict[str, Union[str, List[str]]]]]


class QuickLaunchEntry(TypedDict):
    path: str
    icon: str
    tags: Optional[list[str]]
