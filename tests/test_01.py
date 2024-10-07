# tests/test_01.py

from dataclasses import dataclass, field


def test_dataclasses_inner_class_mutability():
    """
    Tests the mutability of inner classes within dataclasses.
    """

    @dataclass
    class LittleClass:
        """
        A simple inner class with two attributes: a and b.
        """

        a: int = 0
        b: str = "a string"

    @dataclass
    class BigClass:
        """
        A dataclass that contains an instance of LittleClass.
        """

        little: LittleClass = field(default_factory=lambda: LittleClass())

    # Create two instances of BigClass
    big1 = BigClass()
    big2 = BigClass()

    # Assert that the inner LittleClass instances are independent
    assert big1.little.a == 0
    assert big1.little.b == "a string"
    assert big2.little.a == 0
    assert big2.little.b == "a string"

    # Modify the inner LittleClass instance of big2
    big2.little.a = 1
    assert big2.little.a == 1
    assert big1.little.a == 0  # unchanged

    # Create a common LittleClass instance and use it in two BigClass instances
    little_common = LittleClass(a=9, b="common string")
    big3 = BigClass(little=little_common)
    big4 = BigClass(little=little_common)

    # Assert that the common LittleClass instance is shared
    assert big3.little.a == 9
    assert big3.little.b == "common string"
    assert big4.little.a == 9
    assert big4.little.b == "common string"

    # Modify the common LittleClass instance
    big4.little.b = "altered common string"
    assert big4.little.b == "altered common string"
    assert big3.little.b == "altered common string"  # changed


def test_vanilla_inner_class_mutability():
    """
    Tests the mutability of inner classes without using dataclasses.
    """

    class LittleClass:
        """
        A simple inner class with two attributes: a and b.
        """

        def __init__(self, a: int = 0, b: str = "a string"):
            self.a = a
            self.b = b

    class BigClass:
        """
        A class that contains an instance of LittleClass.
        """

        def __init__(self, little: LittleClass = None):
            if little is None:
                self.little = LittleClass()
            else:
                self.little = little

    # Create two instances of BigClass
    big1 = BigClass()
    big2 = BigClass()

    # Assert that the inner LittleClass instances are independent
    assert big1.little.a == 0
    assert big1.little.b == "a string"
    assert big2.little.a == 0
    assert big2.little.b == "a string"

    # Modify the inner LittleClass instance of big2
    big2.little.a = 1
    assert big2.little.a == 1
    assert big1.little.a == 0  # unchanged

    # Create a common LittleClass instance and use it in two BigClass instances
    little_common = LittleClass(a=9, b="common string")
    big3 = BigClass(little=little_common)
    big4 = BigClass(little=little_common)

    # Assert that the common LittleClass instance is shared
    assert big3.little.a == 9
    assert big3.little.b == "common string"
    assert big4.little.a == 9
    assert big4.little.b == "common string"

    # Modify the common LittleClass instance
    big4.little.b = "altered common string"
    assert big4.little.b == "altered common string"
    assert big3.little.b == "altered common string"  # changed


def test_vanilla_mutability():
    """
    Tests the mutability of instances without using dataclasses.
    """

    class ItemForTesting:
        """
        A simple class with several attributes.
        """

        a: int = 0
        b: str = "a string"
        c: list[int] = [1, 2, 3]
        d: list[int] = []
        e: list[str] = ["a", "b", "c"]
        f: list[str] = []
        g: dict[str, int] = {"a": 1, "b": 2}
        h: dict[str, int] = {}

    # Create two instances of ItemForTesting
    item1 = ItemForTesting()
    item2 = ItemForTesting()

    # Assert that the attributes have their default values
    assert item1.a == 0
    assert item1.b == "a string"
    assert item1.c == [1, 2, 3]
    assert item1.d == []
    assert item1.e == ["a", "b", "c"]
    assert item1.f == []
    assert item1.g == {"a": 1, "b": 2}

    # Modify an attribute of item2
    item2.e.append("alteration")
    assert item2.e == ["a", "b", "c", "alteration"]

    # [!] Note that item1.e is also modified because lists are mutable
    assert item1.e == ["a", "b", "c", "alteration"]

    # Assign a new value to item2.e
    item2.e = ["a", "new", "list"]
    assert item2.e == ["a", "new", "list"]
    assert item1.e == ["a", "b", "c", "alteration"]


def test_dataclass_mutability():
    """
    Tests the mutability of dataclass instances.
    """

    @dataclass
    class Item1:
        """
        A dataclass with several attributes.
        """

        a: int = 0
        b: str = "a string"
        c: list[int] = field(default_factory=lambda: [1, 2, 3])
        d: list[int] = field(default_factory=list)
        e: list[str] = field(default_factory=lambda: ["a", "b", "c"])
        f: list[str] = field(default_factory=list)
        g: dict[str, int] = field(default_factory=lambda: {"a": 1, "b": 2})
        h: dict[str, int] = field(default_factory=dict)

    item1 = Item1()
    item2 = Item1()

    # Assert that the attributes have their default values
    assert item1.a == 0
    assert item1.b == "a string"
    assert item1.c == [1, 2, 3]
    assert item1.d == []
    assert item1.e == ["a", "b", "c"]
    assert item1.f == []
    assert item1.g == {"a": 1, "b": 2}
    assert item1.h == {}

    item2.c.append(9)
    assert item2.c == [1, 2, 3, 9]
    assert item1.c == [1, 2, 3]


"""
Module demonstrating the use of dataclasses.

Dataclasses are a simple way to create classes that mainly hold data, 
without requiring boilerplate code like `__init__` and `__repr__` methods.

Note that, although dataclass fields can be type-hinted, these type hints 
do not impose any runtime type constraints. They are meant to serve as 
documentation and can be used by static type checkers.
"""


def test_dataclass_type_constraint():
    @dataclass
    class ItemA:
        a: int
        b: str
        c: float
        d: bool

    ItemA("4464xx", "a", 1.0, True)
