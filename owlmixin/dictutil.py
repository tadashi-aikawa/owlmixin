# coding: utf-8

# Need not unicode_literals
from __future__ import division, absolute_import

import io
import sys
import re
import requests
import codecs
import json
import yaml
from yaml import Loader, SafeLoader

import unicodecsv as csv
from unicodecsv import register_dialect, Dialect, QUOTE_MINIMAL
from typing import List, Union, Optional, Sequence, Dict

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


class CrLfDialect(Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL
register_dialect("crlf", CrLfDialect)


class LfDialect(Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\n'
    quoting = QUOTE_MINIMAL
register_dialect("lf", LfDialect)


PYTHON2 = sys.version_info < (3, 0)


class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def construct_yaml_str(self, node):
    return self.construct_scalar(node)

Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


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


def load_json(data):
    # type (Text) -> Union[dict, list]
    return json.loads(data)


def load_jsonf(fpath, encoding):
    # type (Text, Text) -> Union[dict, list]
    with codecs.open(fpath, encoding=encoding) as f:
        return json.load(f)


def load_yaml(data):
    # type: (Text) -> Union[dict, list]
    return yaml.load(data)


def load_yamlf(fpath, encoding):
    # type: (Text, Text) -> Union[dict, list]
    with codecs.open(fpath, encoding=encoding) as f:
        return yaml.load(f)


def load_csvf(fpath, fieldnames, encoding):
    # type: (Text, Optional[List[Text]], Text) -> List[dict]
    with open(fpath, 'rb') as f:
        snippet = f.read(8192)
        f.seek(0)

        dialect = csv.Sniffer().sniff(snippet if PYTHON2 else snippet.decode(encoding))
        dialect.skipinitialspace = True
        return list(csv.DictReader(f, fieldnames=fieldnames, dialect=dialect, encoding=encoding))


def load_json_url(url):
    # type: (Text) -> Union[dict, list]
    return requests.get(url).json()


def dump_csv(data, fieldnames, with_header=False, crlf=False):
    # type: (List[dict], Sequence[Text], bool, bool) -> Text
    def force_str(v):
        # XXX: Double quotation behaves strangely... so replace (why?)
        return dump_json(v).replace('"', "'") if isinstance(v, (dict, list)) else v

    with io.BytesIO() as sio:
        dialect = 'crlf' if crlf else 'lf'
        writer = csv.DictWriter(sio, fieldnames=fieldnames, encoding='utf8', dialect=dialect)
        if with_header:
            writer.writeheader()
        for x in data:
            writer.writerow({k: force_str(v) for k, v in x.items()})
        sio.seek(0)
        return sio.read().decode('utf8')


def dump_json(data, indent=None):
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
