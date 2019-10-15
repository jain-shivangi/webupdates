#!/usr/bin/env python
__author__ = 'shivangi'

import os
import json
import time
import glob
from webupdates import defaults


def get_files_with_keyword(base_path, prefix="", suffix="", extension=""):
    search_keyword = "{0}*{1}.{2}".format(prefix, suffix, extension)
    f = os.path.join(base_path, search_keyword)
    found = glob.glob(f)
    return found


class FileManager(object):

    BASE_EXT = defaults.DB_EXT
    BACKUP_EXT = defaults.BACKUP_EXT

    def __init__(self, object_name, dirname=defaults.WEBUPDATES_HOME):

        self.dbDirectory = os.path.join(dirname, defaults.DB_DIR_NAME)
        self.backupDirectory = os.path.join(dirname, defaults.BACKUP_DIR_NAME)

        self.object_name = object_name
        self.filename = object_name + "_current.{0}".format(self.BASE_EXT)
        self.filename = os.path.join(self.dbDirectory, self.filename)
        self.backup_file = object_name + time.strftime("%Y%m%d%H%M%S") + ".{0}".format(self.BACKUP_EXT)
        self.backup_file = os.path.join(self.backupDirectory, self.backup_file)

    def copy_contents(self, records):
        try:
            os.makedirs(os.path.dirname(self.filename))
        except:
            pass
        with open(self.filename, "w+") as fh:
            json.dump(obj=records, fp=fh, indent=4)

        try:
            os.makedirs(os.path.dirname(self.backup_file))
        except:
            pass
        with open(self.backup_file, "a+") as fh:
            json.dump(obj=records, fp=fh, indent=4)

    def get_last_page(self):
        if os.path.exists(self.filename):
            with open(self.filename) as fh:
                ret = json.load(fp=fh)
        else:
            found = get_files_with_keyword(
                base_path=defaults.BACKUP_DIR_NAME, prefix=self.object_name, extension=self.BACKUP_EXT
            )
            if found:
                if not found[-1].__contains__(defaults.BACKUP_DIR_NAME):
                    found[-1] = os.path.join(defaults.BACKUP_DIR_NAME, found[-1])
                with open(found[-1], "r") as fh:
                    ret = json.load(fp=fh)[self.object_name]
            else:
                ret = {}
        return ret