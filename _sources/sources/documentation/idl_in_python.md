---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python
---

(idl-in-python)=
# IDL in Python

There is no official mapping from IDL 4.2 to Python at the time of writing. However, Cyclone DDS Python implements (nearly) the full spec by leveraging Python metaclasses and typehints. By doing most of the hard work not in the IDL compiler but by runtime type inspection the generated code actually stays very close to a concept from the Python standard library called `dataclasses`, making it feasible to write types by hand directly in Python and skipping the IDL compiler alltogether, which is convinient when your DDS application is Python-only.

Not everything you can describe in IDL can be captured using basic Python types, and not every basic Python type can be interpreted as IDL. The [`cyclonedds.idl`](cyclonedds.idl) module contains everything needed to make a consistent mapping between the two.

## Mapping

### Basic IDL Types

While Python has only `int`, `str`, `float` and `bool` as relevant basic types in IDL there are integers and floats of varying byte sizes. To leverage these there is the [`cyclonedds.idl.types`](cyclonedds.idl.types) module which specifies these:

```{code-cell} python
from cyclonedds.idl.types import uint8, uint16, uint32, uint64, int8, int16, int32, int64, float32, float64
```

At runtime all integer types will just resolve to the base `int` and the float types to `float`. Also, if you use the base Python `int` in your IDL definitions they will map to `int64` and `float` maps to `float64`. Only the background type inspection will note the byte sizes and use these when reading/writing data. For strings and bools you can use `str` and `bool` as normal.

### Collections

In Python we are used to the `list` and `dict` as our primary datatypes. In IDL there are `sequence`, `array` and `map`, and arguably `bounded_string` is a collection too. Unlike their Python counterparts they are _strongly typed_, meaning that they can only contain items of a specific type. For example, a `sequence<int64>` maps seemlessly to a Python `List[int]` type hint, but the `List[Any]` is not something we can express in IDL. The `array` is something that is not expressable in normal Python type hints at all, fixed-length collections are not a thing in normal Python and using the Python standard library module `array` comes with its own caveats.

Again, we can import these types from [`cyclonedds.idl.types`](cyclonedds.idl.types) and use them in a way that is almost 1-to-1 with IDL. The `map` can simply be expressed as `typing.Dict`.


```{code-cell} python
from cyclonedds.idl.types import sequence, array, bounded_str
from typing import Dict

# sequence, equivalent with a List[int]
a: sequence[int] = [1, 2, 3]

# bounded sequence, List[int] with a max length
b: sequence[int, 3] = [1, 2]

# arrays, fixed length List[int]
c: array[int, 4] = [1, 0, 0, 1]

# maps, simply use typing.Dict
d: Dict[int, str] = {1: "Hello,", 2: "World!"}

# bounded strings are python str with a max length
e: bounded_str[200] = "This will fit."
```

Please note that the specified _bounds_ are not checked by static type checkers or at runtime until the type is serialized.

### Structs

IDL structs are mapped using Python classes that inherit from [`cyclonedds.idl.IdlStruct`](cyclonedds.idl.IdlStruct). They should be fully type-hinted with only legal type constructs as described on this page. In practice you will also want to decorate the class with a `@dataclass` from the standard library module `dataclasses` to autogenerate a constructor.

```{code-cell} python
from cyclonedds.idl import IdlStruct
from dataclasses import dataclass

@dataclass
class MyMessage(IdlStruct):
    msg: str
    sender: str


message = MyMessage(msg="Hi there!", sender="CycloneDDS")
```

Behind the scenes `IdlStruct` is doing the heavy lifting here. It makes sure that the `MyMessage` class can be serialized and deserialized in the [CDR](https://www.omg.org/spec/CORBA) and [XCDRV2](https://www.omg.org/spec/DDS-XTypes/) formats as specified by the [OMG](https://www.omg.org/).

### Enums

The [`IdlEnum`](cyclonedds.idl.IdlEnum) is equivalent to a Python `enum.Enum` with just some behind-the-scenes bookkeeping added that doesn't affect the interface.

```{code-cell} python
from cyclonedds.idl import IdlEnum


class MyEnum(IdlEnum):
    RED = 1
    BLUE = 2
    GREEN = 3

```

### Unions

The Python `typing.Union` doesn't map well to the IDL `union` so there is a separate construct, the [`cyclonedds.idl.IdlUnion`](cyclonedds.idl.IdlUnion). It basically functions as a Python class with a bunch of `Optional` members of which only one can be active at a time. Behind the scenes `IdlUnion` generates a constructor for you so no need to `@dataclass` these types.

IDL unions are _discriminated_, meaning there is a value that keeps track of which member is active. You can also specify a _default_ member, which is active when the discriminator has a value that is not used for any other member. In Python you have to specify this discriminator using the [`case`](cyclonedds.idl.types.case) and [`default`](cyclonedds.idl.types.default) helpers.

```{code-cell} python
from cyclonedds.idl import IdlUnion
from cyclonedds.idl.types import case, default, uint8


class MyUnion(IdlUnion, discriminator=uint8):
    # The case takes a label for the discriminator and a type of the field
    msg: case[0, str]

    # A case can have multiple labels
    userid: case[[1, 2], int]

    # But a default has no labels
    amount: default[int]


# MyUnion will get a generated dataclass-like constructor
a = MyUnion(msg="Hi! We can only fill one member!")
b = MyUnion(userid=404)
c = MyUnion(amount=9001)

print(a.discriminator)  # Would print '0'
# print(a.userid) -> this would error, non-active member!
print(c.discriminator)  # Lowest non-used field, here would be '3'

# You can also manually specify discriminator and value
d = MyUnion(
    discriminator=101,
    value=0  # discriminator 101 -> default amount is active
)
```

For the discriminator you can use up to 4-byte integer types (`int8`, `uint8`, `int16`, `uint16` `int32`, `uint32`) or an `IdlEnum`.

### Bitmasks

In Python an `IdlBitmask` is nothing more than a `@dataclass` with only booleans. You can use this instead of a normal `IdlStruct` when size matters. A normal `bool` in a `IdlStruct` uses a whole byte when serialized. In an `IdlBitmask` the bools are serialized into a single integer which can reduce the size dramatically if you need to send _a lot_ of booleans.

```{code-cell} python
from cyclonedds.idl import IdlBitmask
from dataclasses import dataclass

@dataclass
class MyBitmask(IdlBitmas):
    all: bool
    of: bool
    the: bool
    booleans: bool
    but: bool
    no: bool
    other: bool
    types: bool
```

## Annotations

Annotations are the IDL way to add extra information about a type. The Python implementation of these lives in [`cyclonedds.idl.annotations`](cyclonedds.idl.annotations).

### @key

Arguably the most important annotation is `@key` which designates a member of a `IdlStruct` as part of the _key_ for a type. The _key_ of a type determines which _instance_ a _sample_ belongs to. For more details on this see [Keys, Instances and Samples](keys-instances-samples).

To apply `@key` to a struct member in Python call the [`key`](cyclonedds.idl.annotations.key) annotation function inside the class definition scope:

```{code-cell} python
from cyclonedds.idl import IdlStruct
from cyclonedds.idl.types import uint64
from cyclonedds.idl.annotate import key
from dataclasses import dataclass

@dataclass
class MyMessage(IdlStruct):
    msg_id: int
    key(msg_id)
    msg: str
    sender: str

message = MyMessage(msg_id=11, msg="Hi there!", sender="CycloneDDS")
```

In IDL you can also apply `@key` to a union discriminator. In Python this is captured by using the `discriminator_is_key` class argument:

```{code-cell} python
from cyclonedds.idl import IdlUnion
from cyclonedds.idl.types import case, default, uint8


class MyUnion(IdlUnion, discriminator=uint8, discriminator_is_key=True):
    msg: case[0, str]
    userid: case[[1, 2], int]
    amount: default[int]

```