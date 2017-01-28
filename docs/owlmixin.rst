OwlMixin
========

.. note::

    Usage on each methods are valid on the premise that the following classes is defined in advance.

    .. code-block:: python

        from typing import Optional
        from owlmixin import OwlMixin, TList, TDict

        class Food(OwlMixin):
            def __init__(self, name, names_by_lang=None, **extra):
                self.name = name  # type: unicode
                self.names_by_lang = names_by_lang  # type: Optional[TDict[unicode, unicode]]

        class Human(OwlMixin):
            def __init__(self, id, name, favorites):
                self.id = id  # type: int
                self.name = name  # type: unicode
                self.favorites = Food.from_dicts(favorites)  # type: TList[Food]

        class Machine(OwlMixin):
            def __init__(self, id, name):
                self.id = id  # type: int
                self.name = name  # type: unicode

.. testsetup:: *

    from typing import Optional
    from owlmixin import OwlMixin, TList, TDict

    class Food(OwlMixin):
        def __init__(self, name, names_by_lang=None, **extra):
            self.name = name  # type: unicode
            self.names_by_lang = names_by_lang  # type: Optional[TDict[unicode, unicode]]

    class Human(OwlMixin):
        def __init__(self, id, name, favorites):
            self.id = id  # type: int
            self.name = name  # type: unicode
            self.favorites = Food.from_dicts(favorites)  # type: TList[Food]

    class Machine(OwlMixin):
        def __init__(self, id, name):
            self.id = id  # type: int
            self.name = name  # type: unicode

.. automodule:: owlmixin
    :members:
    :undoc-members:
