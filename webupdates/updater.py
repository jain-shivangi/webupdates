#!/usr/bin/env python
__author__ = 'shivangi'

import xml
import xmltodict
from collections import OrderedDict
from _private.reader import RequestReader
from _private.webpages import Webpage
import defaults


class WebUpdates(object):

    updates = OrderedDict()

    def __init__(self, **kwargs):
        """
        :param json_input     : Input JSON file to process requests. Default pipe to samples.
        :param json_output    : Output JSON file, having new updates. Default pipe to USER_HOME.
        :param data_path      : It's book-keeping directory where html pages & old-updates are stored.
        """
        self.json_input_file = kwargs.get('json_input', defaults.JSON_INPUT)
        self.json_output_file = kwargs.get('json_output', defaults.JSON_OUTPUT)
        self.data_path = kwargs.get('data_path', defaults.USER_HOME)

    def build_request(self, json_input=defaults.JSON_INPUT, mandatory_tags=defaults.MANDATORY_TAGS, validation_index=1):
        """
        Parses & Validates the JSON Input file.
        Validation checks for the Mandatory tags needed to be specified in the JSON input file.

        :param json_input: Optional. JSON Input file. (Check sample JSON request file)
        :param mandatory_tags: List of tags needed to be validated.
        :param validation_index: In parsed dictionary checks the childs on specified index for validation.
        :return: request: Translated & Validated dictionary for JSON Input.
        """
        if json_input:
            self.json_input_file = json_input
        readRequest = RequestReader(json_file=self.json_input_file)
        readRequest.read_request()
        request = readRequest.get_request()
        if mandatory_tags:
            if not readRequest.validate_request(tags=mandatory_tags, index=validation_index):
                raise NotImplementedError("Not all mandatory tags found in JSON file.")
        return request

    def get_pages(self, request):
        """
        :param request: Translated & Validated dictionary for JSON Input.
        :return: 'pages' return an information dictionary.
        'pages':{
            'object':     Webpage(url) object,
            'pattern':    pattern tag from json file,
            'record':     record tags for parsed HTML file,
            'attributes': attribute tags with the details of HTML tag locators.
        }
        """
        pages = OrderedDict()
        for page_name, page_details in request.items():
            page = Webpage(url=page_details['url'])
            if not pages.has_key(page_name):
                pages[page_name] = OrderedDict()
            pages[page_name]['object'] = page
            pages[page_name]['pattern'] = page_details['pattern'] = page.get_patterns(pattern=page_details['pattern'])
            pages[page_name]['record'] = ['group'] + page_details['record'].split(',')
            for attr, vals in page_details['attributes'].items():
                page_details['attributes'][attr] = vals.split(',')
            pages[page_name]['attributes'] = page_details['attributes']
            pages[page_name]['parsed'] = self.adjust_xml(page_details)['parsed']
        return pages

    @staticmethod
    def adjust_xml(details):
        """
        Reformats the XML where-ever the tags are missing.
        """
        flag = 0
        while True:
            to_parse = "<group>" + details['pattern'][0] + "</group>"
            try:
                parsed = xmltodict.parse(to_parse)
                details['parsed'] = parsed
                break
            except xml.parsers.expat.ExpatError as e:
                # print("Fixing the string")
                try:
                    line_no = int(e.message.split('line')[1].split(',')[0])
                    details_list = details['pattern'][0].split('\n')
                    details_list[line_no-2] = details_list[line_no-2].replace(">", "/>")
                    details['pattern'][0] = "\n".join(details_list)
                    flag = 0
                except Exception as err:
                    flag += 1
            except Exception as e:
                print("[ERROR] {0} - {1}".format(e.__class__.__name__, e.message))
                break
            if flag > 1:
                details['parsed'] = {}
                break
        return details

    def get_records(self, pages):
        """
        Process the pages and gets the record in format as:
        RECORDS:{
            PageName1: {
                Attr1: Val1,
                Attr2: Val2,
                Att3: Val3,...
            },
            ....
        }
        :param pages:
        :return: Rcords.
        """
        records = OrderedDict()

        def get_record(parsed, record_tags, attributes):
            record = parsed

            # Get Record value as the Record tags.
            for tag in record_tags:
                record = record[tag]

            if not isinstance(record, list):
                record = [record]

            processed = list()

            for record_ in record:
                R = OrderedDict()
                for attribute_name, attribute_value in attributes.items():
                    if not R.has_key(attribute_name):
                        R[attribute_name] = None
                    temp = record_
                    for val in attribute_value:
                        try:
                            try:
                                temp = temp[int(val)]
                            except:
                                temp = temp[val]
                        except:
                            temp = None
                            break
                    R[attribute_name] = temp
                processed.append(R)
            return processed

        for record_name, record_details in pages.items():
            try:
                records[record_name] = get_record(
                        parsed=record_details['parsed'],
                        record_tags=record_details['record'],
                        attributes=record_details['attributes']
                    )
            except Exception as err:
                print(err.__class__.__name__, err.message)
                records[record_name] = {}
        return records