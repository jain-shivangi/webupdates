#!/usr/bin/env python
__author__ = 'shivangi'

import os
import time
import sys
import json
import defaults
from collections import OrderedDict
from updater import WebUpdates
from _private import get_parser
from _private import FileManager

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_timestamp():
    return time.strftime("%Y%m%d%H%M%S")


def print_updates(updates, spaces=20):
    print("\nUpdates are as follows...")
    try:
        for page, update in updates.items():
            s = "="*5 + page + "="*5
            print(s)
            for up in update:
                if isinstance(up, dict):
                    for k, v in up.items():
                        k = k + ':' + ' '*(spaces - len(k))
                        print("{0}:\t{1}".format(k, v))
                print("-"*len(s))
            print("="*(len(s)))
    except Exception as err:
        pass


def main():
    parser = get_parser()
    args = parser.parse_args()
    """
    Arguments:
    json_input     = Input JSON file to process requests. Default pipe to samples.
    json_output    = Output JSON file, having new updates. Default pipe to USER_HOME.
    watch          = Boolean. Run this as daemon process.
    after_every    = Polls the requested page after X secs.
    data_path      = It's book-keeping directory where html pages & old-updates are stored.
    """
    if not os.path.exists(args.json_input):
        print("ERROR in arguments.")
        sys.exit(-1)
    try:
        os.makedirs(args.data_path)
    except:
        pass
    try:
        updates = configure_and_get_updates(args.json_input, args.json_output, args.data_path, args.watch, args.secs, args.daemonize)
    except Exception as err:
        print("ERROR - {0}: {1}".format(err.__class__.__name__, err.message))
        sys.exit(-1)
    if not args.off_console:
        print_updates(updates)
    else:
        return updates


def get_saved_updates(record_name, data_path):
    fm = FileManager(record_name, data_path)
    try:
        ret = fm.get_last_page()
    except Exception as e:
        ret = {}
    return ret


def save_and_create_backups(records, json_output, data_path):

    for record_name, records_ in records.items():
        fm = FileManager(record_name, data_path)
        fm.copy_contents(records_)

    with open(json_output, "w+") as fh:
        json.dump(records, fh, indent=4)


def compare_dictionaries(subtractants, subtractors):
    updates = list()
    for subtractant in subtractants:
        flag = False
        for subtractor in subtractors:
            if subtractant == subtractor:
                flag = True
                break
        if not flag:
            updates.append(subtractant)
    return updates


def configure_and_get_updates(
        json_input, json_output=defaults.JSON_INPUT,
        data_path=defaults.WEBUPDATES_HOME,
        watch=False, secs=defaults.DEFAULT_UPDATE_TIME,
        daemonize=False):
    """
    Function which can be configured as per the parameters.
    RECORDS:{
            PageName1: {
                Attr1: Val1,
                Attr2: Val2,
                Att3: Val3,...
            },
            ....
        }
    :param json_input: JSON input file.
    :param json_output: JSON Output file. (Consolidated results in JSON file)
    :param data_path: Configurable workspace where project associated data is stored.
    :param watch: Boolean, specifies the function to work as watch-dog. i.e Polling for updates is enabled.
    :param secs: Time in seconds for Polling period.
    :return: Records.
    """
    if not daemonize:
        try:
            while True:
                records = get_updates(json_input)
                Updates = OrderedDict()

                for record_name, record in records.items():
                    last_updates = get_saved_updates(record_name, data_path)
                    Updates[record_name] = compare_dictionaries(subtractants=records[record_name], subtractors=last_updates)

                save_and_create_backups(records, json_output, data_path)

                if not watch:
                    return Updates
                else:
                    time.sleep(secs)
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit(-1)


def get_updates(json_input):
    """
    Simple function which get updates as Records.
    RECORDS:{
            PageName1: {
                Attr1: Val1,
                Attr2: Val2,
                Att3: Val3,...
            },
            ....
        }
    :param json_input: JSON input file.
    :return: Records.
    """

    update = WebUpdates()

    try:
        requests_ = update.build_request(json_input=json_input)
    except Exception as err:
        print("ERROR: While building request [{0}:{1}]".format(err.__class__.__name__, err.message))
        if err.__class__ == NotImplementedError:
            print("Check README to know more about the required tags in JSON.")
        sys.exit(-1)

    try:
        pages = update.get_pages(request=requests_)
    except Exception as err:
        print("ERROR: While gathering pages [{0}:{1}]".format(err.__class__.__name__, err.message))
        sys.exit(-1)

    try:
        records = update.get_records(pages=pages)
    except Exception as err:
        print("ERROR: While gathering records [{0}:{1}]".format(err.__class__.__name__, err.message))
        sys.exit(-1)

    return records


if __name__ == "__main__":
    r = main()
    if r == -1:
        sys.exit(r)
    print_updates(r)