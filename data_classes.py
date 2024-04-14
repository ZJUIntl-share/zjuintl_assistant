"""
This file contains the data classes used to store parsed data from spider
"""

import datetime
from dataclasses import dataclass


@dataclass
class BB_DueAssignment:
    """
    Class to store due assignment data
    """
    course: str
    title: str
    date: datetime.datetime


@dataclass
class BB_Grade:
    """
    Class to store grade data
    """
    course: str
    title: str
    pointsPossible: float
    grade: float
    date: datetime.datetime


@dataclass
class Announcement:
    """
    Class to store announcement data
    """
    title: str
    course: str
    html_content: str
    date: datetime.datetime
