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
    event_type: str

    def get_event_message(self):
        return EVENT_TYPE_MAP[self.event_type]


@dataclass
class MyZJU_Notice:
    """
    Class to store myZJU notice data
    """
    title: str
    link: str
    content: str
    date: datetime.datetime


EVENT_TYPE_MAP = {
    'SU:SU_SUBMIT': 'Survey Submitted',
    'WK:WK_GR_ATTEMPT': 'Group Wiki Needs Grading',
    'AS:DUE': 'Assignment Due',
    'DF:DF_GR_ATTEMPT': 'Group Forum Needs Grading',
    'CM:CM_RCVD': 'Course Message Received',
    'AS:AS_GA_AVAIL_RESEND': 'Assignment Group Assignment Available Resend',
    'SU:SU_AVAIL': 'Survey Available',
    'AS:OVERDUE': 'Assignment Overdue',
    'SU:OVERDUE': 'Survey Overdue',
    'GB:OVERDUE': 'Item Overdue',
    'DT:DT_GR_ATTEMPT': 'Group Thread Needs Grading',
    'JN:JN_ATTEMPT': 'Journal Needs Grading',
    'WK:WK_ATTEMPT': 'Wiki Needs Grading',
    'SC:SC_SUBMIT': 'Assessment Needs Grading',
    'SC:OVERDUE': 'Item Overdue',
    'AS:AS_GA_ATTEMPT': 'Group Assignment Needs Grading',
    'SC:SC_SUBMIT_LATE': 'Assessment Needs Grading (Submitted Late)',
    'TE:OVERDUE': 'Assessment Overdue',
    'CR:CR_AVAIL': 'Course or Organization Available',
    'TE:TE_SUBMIT_LATE': 'Assessment Needs Grading (Submitted Late)',
    'QU:QU_AVAIL': 'Quota Available',
    'AS:AS_AVAIL': 'Assignment Available',
    'SC:SC_GRA_UPDATED': 'Manual Grade Updated',
    'SC:DUE': 'Item Due',
    'TE:TE_AVAIL': 'Assessment Available',
    'TE:TE_SUBMIT': 'Assessment Needs Grading',
    'GB:DUE': 'Item Due',
    'DT:DT_ATTEMPT': 'Thread Needs Grading',
    'CO:CO_AVAIL': 'Content Available',
    'SU:DUE': 'Survey Due',
    'BL:BL_ATTEMPT': 'Blog Needs Grading',
    'GB:GB_ATT_UPDATED': 'Attempt Grade Updated',
    'AS:AS_GA_AVAIL': 'Assignment Group Assignment Available',
    'AS:AS_LATE_ATTEMPT': 'Assignment  Needs Grading (Submitted Late)',
    'TE:TE_AVAIL_RESEND': 'Assessment Attempt Available Resent',
    'DF:DF_ATTEMPT': 'Forum Needs Grading',
    'GB:GB_NEEDS_RECON': 'Column Needs Reconciliation',
    'SC:SC_AVAIL': 'alerts.stream.scorm.due.setting',
    'AS:AS_GA_LATE_ATTEMPT': 'Group Assignment Needs Grading (Submitted Late)',
    'TE:DUE': 'Assessment Due',
    'JN:JN_GR_ATTEMPT': 'Group Journal Needs Grading',
    'AN:AN_AVAIL': 'Announcement Available',
    'AS:AS_ATTEMPT': 'Assignment Needs Grading',
    'GB:GB_GRA_UPDATED': 'Manual Grade Updated',
    'AS:AS_AVAIL_RESEND': 'Assignment Available Resend',
    'BL:BL_GR_ATTEMPT': 'Group Blog Needs Grading',
    'GB:GB_GRA_CLEARED': 'Manual Grade Cleared'
}
