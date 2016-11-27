# dictmixin

[![](https://api.travis-ci.org/tadashi-aikawa/dictmixin.svg?branch=master)](https://travis-ci.org/tadashi-aikawa/dictmixin)
[![](https://coveralls.io/repos/github/tadashi-aikawa/dictmixin/badge.svg)](https://coveralls.io/github/tadashi-aikawa/dictmixin)

Parsing mixin which converts `data class instance`, `dict object`, `json string` and `yaml string` each other.

|   from   |    to    |                      method                     |
|----------|----------|-------------------------------------------------|
| instance | dict     | `to_dict`                                       |
| instance | json     | `to_json`, `to_pretty_json`                     |
| instance | yaml     | -                                               |
| dict     | instance | `from_dict`, `from_dict2list`, `from_dict2dict` |
| dict     | json     | -                                               |
| dict     | yaml     | -                                               |
| json     | instance | `from_json`                                     |
| json     | dict     | -                                               |
| json     | yaml     | -                                               |
| yaml     | instance | `from_yaml`                                     |
| yaml     | dict     | -                                               |
| yaml     | json     | -                                               |
