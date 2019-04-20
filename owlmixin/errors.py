# coding: utf-8
from typing import List


class OwlMixinError(Exception):
    title: str
    description: str

    def __str__(self) -> str:
        return f"""
.        ∧,,_∧      ,___________________
     ⊂ ( ･ω･ )つ-  <  {self.title}
   ／／/     /::/     `-------------------
   |::|/⊂ヽノ|::|」
／￣￣旦￣￣￣／|
＿＿＿＿＿＿／  | |
|------ー----ー|／

{self.description}
        """


class InvalidTypeError(OwlMixinError):
    """
    :ivar str title: Error title
    :ivar str description: Error description
    :ivar str cls: Class name
    :ivar str prop: Property name
    :ivar any value: Property value
    :ivar List[str] expected: Expected types
    :ivar str actual: Actual type
    """
    title: str = "Invalid Type error"
    cls: str
    prop: str
    value: any
    expected: List[str]
    actual: str

    def __init__(self, cls, prop: str, value: any, expected: list, actual):
        self.cls = f"{cls.__module__}.{cls.__name__}"
        self.prop = prop
        self.value = value
        self.expected = [t.__name__ for t in expected]
        self.actual = actual.__name__

    @property
    def description(self) -> str:
        # expected_typestr = " or ".join((str(t) for t in expected))
        return f"""`{self.cls}#{self.prop} = {self.value}` doesn't match expected types.
Expected type is one of {self.expected}, but actual type is `{self.actual}`

    * If you want to force cast, set `force_cast=True`
    * If you don't want to force cast, specify value which has correct type"""


class UnknownPropertiesError(OwlMixinError):
    """
    :ivar str title: Error title
    :ivar str description: Error description
    :ivar str cls: Class name
    :ivar List[str] props: Unknown property names
    """
    title: str = "Unknown properties error"
    cls: str
    props: List[str]

    def __init__(self, cls, props: str):
        self.cls = f"{cls.__module__}.{cls.__name__}"
        self.props = props

    @property
    def description(self) -> str:
        return f"""`{self.cls}` has unknown properties {self.props}!!

    * If you want to allow unknown properties, set `restrict=False`
    * If you want to disallow unknown properties, add {' and '.join(
            ['`' + x + '`' for x in self.props])} to {self.cls}"""


class RequiredError(OwlMixinError):
    """
    :ivar str title: Error title
    :ivar str description: Error description
    :ivar str cls: Class name
    :ivar str prop: Property name
    :ivar str type_: Property type
    """
    title: str = "Required error"
    cls: str
    prop: str
    type_: str

    def __init__(self, cls, prop: str, type_):
        self.cls = f"{cls.__module__}.{cls.__name__}"
        self.prop = prop
        self.type_ = f"{type_.__name__}"

    @property
    def description(self) -> str:
        return f"""`{self.cls}#{self.prop}: {self.type_}` is empty!!

    * If `{self.prop}` is certainly required, specify anything.
    * If `{self.prop}` is optional, change type from `{self.type_}` to `TOption[{self.type_}]`"""
