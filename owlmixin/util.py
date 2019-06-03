# coding: utf-8

# The location of `import yaml` is not optimized!!
# pylint: disable=wrong-import-order,duplicate-code

import codecs
import csv
import io
import json
import re
from typing import List, Dict, Union, Sequence, Iterable, Iterator
from urllib.request import urlopen

import yaml
from math import floor, ceil
from unicodedata import east_asian_width


class CrLfCsvDialect(csv.Dialect):
    delimiter = ","
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


class CrLfTsvDialect(csv.Dialect):
    delimiter = "\t"
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


class LfCsvDialect(csv.Dialect):
    delimiter = ","
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = "\n"
    quoting = csv.QUOTE_MINIMAL


class LfTsvDialect(csv.Dialect):
    delimiter = "\t"
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = "\n"
    quoting = csv.QUOTE_MINIMAL


csv.register_dialect("crlf_csv", CrLfCsvDialect)
csv.register_dialect("crlf_tsv", CrLfTsvDialect)
csv.register_dialect("lf_csv", LfCsvDialect)
csv.register_dialect("lf_tsv", LfTsvDialect)


def get_dialect_name(crlf: bool, tsv: bool) -> str:
    line_break = "crlf" if crlf else "lf"
    file = "tsv" if tsv else "csv"
    return f"{line_break}_{file}"


class MyDumper(yaml.SafeDumper):
    # pylint: disable=too-many-ancestors
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def construct_yaml_str(self, node):
    return self.construct_scalar(node)


yaml.SafeLoader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)


def replace_keys(d, keymap, force_snake_case):
    """
    :param dict d:
    :param Dict[unicode, unicode] keymap:
    :param bool force_snake_case:
    :rtype: Dict[unicode, unicode]
    """
    return {
        to_snake(keymap.get(k, k)) if force_snake_case else keymap.get(k, k): v
        for k, v in d.items()
    }


def to_snake(value):
    """For key of dictionary

    :param unicode value:
    :rtype: unicode
    """
    return re.sub(r"((?<!^)[A-Z])", "_\\1", value.strip("<>-")).lower().replace("-", "_")


def load_json(json_str):
    """
    :param unicode json_str:
    :rtype: dict | list
    """
    return json.loads(json_str)


def load_jsonf(fpath, encoding):
    """
    :param unicode fpath:
    :param unicode encoding:
    :rtype: dict | list
    """
    with codecs.open(fpath, encoding=encoding) as f:
        return json.load(f)


def load_yaml(yaml_str):
    """
    :param unicode yaml_str:
    :rtype: dict | list
    """
    return yaml.safe_load(yaml_str)


def load_yamlf(fpath, encoding):
    """
    :param unicode fpath:
    :param unicode encoding:
    :rtype: dict | list
    """
    with codecs.open(fpath, encoding=encoding) as f:
        return yaml.safe_load(f)


def load_csvf(fpath: str, fieldnames: List[str], encoding: str) -> Iterator[dict]:
    """
    :param fpath:
    :param fieldnames:
    :param encoding:
    :return Iterator of dict:
    """
    with open(fpath, mode="r", encoding=encoding) as f:
        snippet = f.read(8192)
        f.seek(0)

        dialect = csv.Sniffer().sniff(snippet)
        dialect.skipinitialspace = True
        reader = csv.DictReader(f, fieldnames=fieldnames, dialect=dialect)
        for d in reader:
            yield d


def load_json_url(url):
    """
    :param unicode url:
    :rtype: dict | list
    """
    return json.loads(urlopen(url).read())


def dump_csv(
    data: Iterable[dict],
    fieldnames: Sequence[str],
    *,
    with_header: bool = False,
    crlf: bool = False,
    tsv: bool = False,
) -> str:
    """
    :param data:
    :param fieldnames:
    :param with_header:
    :param crlf:
    :param tsv:
    :return: Csv string
    """

    def force_str(v):
        # XXX: Double quotation behaves strangely... so replace (why?)
        return dump_json(v).replace('"', "'") if isinstance(v, (dict, list)) else v

    with io.StringIO() as sio:
        dialect = get_dialect_name(crlf, tsv)
        writer = csv.DictWriter(sio, fieldnames=fieldnames, dialect=dialect, extrasaction="ignore")
        if with_header:
            writer.writeheader()
        for x in data:
            writer.writerow({k: force_str(v) for k, v in x.items()})
        sio.seek(0)
        return sio.read()


def dump_csvf(
    data: Iterable[any],
    fieldnames: Sequence[str],
    *,
    fpath: str,
    encoding: str,
    with_header: bool = False,
    crlf: bool = False,
    tsv: bool = False,
) -> str:
    """
    :param data:
    :param fieldnames:
    :param fpath: write path
    :param encoding: encoding
    :param with_header:
    :param crlf:
    :param tsv:
    :return: written path
    """

    def force_str(v):
        # XXX: Double quotation behaves strangely... so replace (why?)
        return dump_json(v).replace('"', "'") if isinstance(v, (dict, list)) else v

    with codecs.open(fpath, mode="w", encoding=encoding) as f:
        dialect = get_dialect_name(crlf, tsv)
        writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=dialect, extrasaction="ignore")
        if with_header:
            writer.writeheader()
        for x in data:
            writer.writerow({k: force_str(v) for k, v in x.items()})

    return fpath


def dump_json(data, indent=None):
    """
    :param list | dict data:
    :param Optional[int] indent:
    :rtype: unicode
    """
    return json.dumps(
        data, indent=indent, ensure_ascii=False, sort_keys=True, separators=(",", ": ")
    )


def dump_jsonf(data: Union[list, dict], *, fpath: str, encoding: str, indent=None) -> str:
    """
    :param data: list | dict data
    :param fpath: write path
    :param encoding: encoding
    :param indent:
    :rtype: written path
    """
    with codecs.open(fpath, mode="w", encoding=encoding) as f:
        f.write(dump_json(data, indent))
        return fpath


def dump_yaml(data):
    """
    :param list | dict data:
    :rtype: unicode
    """
    return yaml.dump(
        data, indent=2, encoding=None, allow_unicode=True, default_flow_style=False, Dumper=MyDumper
    )


def dump_yamlf(data: Union[list, dict], *, fpath: str, encoding: str) -> str:
    """
    :param data: list | dict data
    :param fpath: write path
    :param encoding: encoding
    :rtype: written path
    """
    with codecs.open(fpath, mode="w", encoding=encoding) as f:
        f.write(dump_yaml(data))
        return fpath


def dump_table(data: List[dict], fieldnames: Sequence[str]) -> str:
    """
    :param data:
    :param fieldnames:
    :return: Table string
    """

    def min3(num: int) -> int:
        return 3 if num < 4 else num

    width_by_col: Dict[str, int] = {
        f: min3(max([string_width(str(d.get(f))) for d in data] + [string_width(f)]))
        for f in fieldnames
    }

    def fill_spaces(word: str, width: int, center=False):
        """ aaa, 4 => ' aaa  ' """
        to_fills: int = width - string_width(word)
        return (
            f" {' ' * floor(to_fills / 2)}{word}{' ' * ceil(to_fills / 2)} "
            if center
            else f" {word}{' ' * to_fills} "
        )

    def to_record(r: dict) -> str:
        return (
            f"|{'|'.join([fill_spaces(str(r.get(f)), width_by_col.get(f)) for f in fieldnames])}|"
        )

    lf = "\n"
    return f"""
|{'|'.join([fill_spaces(x, width_by_col.get(x), center=True) for x in fieldnames])}|
|{'|'.join([fill_spaces(width_by_col.get(x) * "-", width_by_col.get(x)) for x in fieldnames])}|
{lf.join([to_record(x) for x in data])}
""".lstrip()


def string_width(word: str) -> int:
    """
    :param word:
    :return: Widths of word

    Usage:

        >>> string_width('abc')
        3
        >>> string_width('Ａbしー')
        7
        >>> string_width('')
        0
    """
    return sum(map(lambda x: 2 if east_asian_width(x) in "FWA" else 1, word))
