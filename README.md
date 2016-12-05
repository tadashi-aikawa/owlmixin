# dictmixin

[![](https://api.travis-ci.org/tadashi-aikawa/dictmixin.svg?branch=master)](https://travis-ci.org/tadashi-aikawa/dictmixin)
[![Test Coverage](https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/coverage.svg)](https://codeclimate.com/github/tadashi-aikawa/dictmixin/coverage)
[![Code Climate](https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/gpa.svg)](https://codeclimate.com/github/tadashi-aikawa/dictmixin)
[![](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![](https://img.shields.io/badge/python-2.7/3.3/3.4/3.5-blue.svg)]()

Parsing mixin which converts `data class instance`, `dict object`, `json string` and `yaml string` each other.

## Installation

```
pip install git+https://github.com/tadashi-aikawa/dictmixin@0.3.0
```

## API

|   from   |    to    |                      method                     |
|----------|----------|-------------------------------------------------|
| instance | dict     | `to_dict`                                       |
| instance | json     | `to_json`, `to_pretty_json`                     |
| instance | yaml     | `to_yaml`                                       |
| dict     | instance | `from_dict`, `from_dict2list`, `from_dict2dict` |
| dict     | json     | -                                               |
| dict     | yaml     | -                                               |
| json     | instance | `from_json`                                     |
| json     | dict     | -                                               |
| json     | yaml     | -                                               |
| yaml     | instance | `from_yaml`                                     |
| yaml     | dict     | -                                               |
| yaml     | json     | -                                               |

