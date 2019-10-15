#!/usr/bin/env python
__author__ = 'shivangi'

"""
Default paramters for the tools are initialized in this file.
BASE_DIR:          Defines the Base Path of the project, where ever it resides.
USER_HOME:         Depending upon the OS, it gets the Home path for the logged in user.
                     In Windows, its: CUsersusername
WEBUPDATES_HOME:   Creates a workspace after installing the project in USER_HOME/ where ever user describes.
*_EXTs:            Defines extensions for different files.
"""

import os


sample_json = u"""
{
  "ZeroDay":{
    "url": "http://www.zdnet.com/blog/security/",
    "pattern": "<div class=\\"river\\">\\n[ ]*<div>((?:\\n.*)*)<nav class=\\"pagination\\">",
    "record": "div,article",
    "attributes":{
      "Title": "div,div,1,h3,a,#text",
      "Author": "div,div,1,p,1,a,#text",
      "Summary": "div,div,1,p,0,#text",
      "Date": "div,div,1,p,1,span,0,@data-date",
      "Article-link": "div,div,1,h3,a,@href"
    }
  },
  "HackerNews":{
    "url": "https://thehackernews.com/",
    "pattern": "<div class='blog-posts clear'>((?:\\n.*)*)</div>\\n*[ ]*<div[ ]*class='sticky-stopper'>",
    "record": "div",
    "attributes":{
      "Title": "a,div,div,1,h2,#text",
      "Date": "a,div,div,1,div,0,#text",
      "Summary": "a,div,div,1,div,1,#text",
      "Article-link": "a,@href",
      "Author": "a,div,div,1,div,0,span,#text"
    }
  }
}
"""


BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

USER_HOME = os.path.expanduser('~')
WEBUPDATES_HOME = os.path.join(USER_HOME, "WebUpdates")

DB_DIR_NAME = "db"
DB_EXT = "info"
BACKUP_DIR_NAME = "backup"
BACKUP_EXT = "backup"

JSON_INPUT = os.path.join(os.path.join(os.path.join(BASE_DIR, "tests"), "samples"), "request.json")
try:
    os.makedirs(os.path.dirname(JSON_INPUT))
except:
    pass

with open(JSON_INPUT, "w+") as fh:
    fh.write(sample_json)

JSON_OUTPUT = os.path.join(WEBUPDATES_HOME, "updates.json")


DEFAULT_UPDATE_TIME = 30*60


MANDATORY_TAGS = [
    u"url",
    u"pattern",
    u"record",
    u"attributes",
]
