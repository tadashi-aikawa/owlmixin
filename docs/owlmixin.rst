API Reference
=============

For usage section is fine on the premise that the following classes is defined in advance.

.. code-block:: python

    class Food(OwlMixin):
        def __init__(self, name, names_by_lang=None):
            self.name = name  # type: unicode
            self.names_by_lang = names_by_lang  # type: Optional[TDict[unicode, unicode]]

    class Human(OwlMixin):
        def __init__(self, id, name, favorites):
            self.id = id  # type: int
            self.name = name  # type: unicode
            self.favorites = Food.from_dicts(favorites)  # type: TList[Food]

.. testsetup:: *

    from typing import Optional
    from owlmixin import OwlMixin, TList

    class Food(OwlMixin):
        def __init__(self, name, names_by_lang=None):
            self.name = name  # type: unicode
            self.names_by_lang = names_by_lang  # type: Optional[TDict[unicode, unicode]]

    class Human(OwlMixin):
        def __init__(self, id, name, favorites):
            self.id = id  # type: int
            self.name = name  # type: unicode
            self.favorites = Food.from_dicts(favorites)  # type: TList[Food]


.. automodule:: owlmixin
    :members:
    :undoc-members:
