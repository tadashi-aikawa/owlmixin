# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import re
import csv
import requests
import json
import yaml
from yaml import Loader, SafeLoader

from typing import List, Union, Optional, Iterable, Dict

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


def replace_keys(d, keymap, force_snake_case):
    # type: (dict, Dict[Text, Text], bool) -> Dict[Text, Text]
    return {
        to_snake(keymap.get(k, k)) if force_snake_case else keymap.get(k, k):
            v for k, v in d.items()
        }


def to_snake(value):
    # type: (Text) -> Text
    # For key of dictionary
    return re.sub(r'((?<!^)[A-Z])', "_\\1", value).lower().replace("-", "_")


class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def construct_yaml_str(self, node):
    return self.construct_scalar(node)


Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def load_json(data):
    # type (Text) -> dict
    return json.loads(data)


def load_yaml(data):
    # type: (Union[Text, file]) -> dict
    return yaml.load(data)


def load_csv(csvfile, fieldnames):
    # type: (Text, Optional[List[Text]]) -> List[dict]
    with open(csvfile) as f:
        snippet = f.read(8192)
        f.seek(0)

        dialect = csv.Sniffer().sniff(snippet)
        dialect.skipinitialspace = True
        return list(csv.DictReader(f, fieldnames=fieldnames, dialect=dialect))


def load_json_url(url):
    # type: (Text) -> Union[dict, list]
    return requests.get(url).json()


def dump_json(data, indent):
    # type: (Union[dict, list], int) -> Text
    return json.dumps(data,
                      indent=indent,
                      ensure_ascii=False,
                      sort_keys=True,
                      separators=(',', ': '))


def dump_yaml(data):
    # type: (Union[dict, list]) -> Text
    return yaml.dump(data,
                     indent=2,
                     encoding=None,
                     allow_unicode=True,
                     default_flow_style=False,
                     Dumper=MyDumper)
