# cyclonedds.idl.types

Sometimes a normal python `int` won't do, you need an integer of a specific type. The `idl.types` module provides extra types on top of the regular Python types so you can express all IDL constructs.

```{eval-rst}

.. autodata:: cyclonedds.idl.types.NoneType

    The type of `None`, similar to `void` in C.

.. autoclass:: cyclonedds.idl.types.array

.. autoclass:: cyclonedds.idl.types.sequence

.. autoclass:: cyclonedds.idl.types.typedef

.. autoclass:: cyclonedds.idl.types.bounded_str

.. autoclass:: cyclonedds.idl.types.case

.. autoclass:: cyclonedds.idl.types.default

.. py:data:: cyclonedds.idl.types.char
    :type: type

    String with length=1. At runtime is represented as Python ``str``.

.. py:data:: cyclonedds.idl.types.int8
    :type: type

    Signed 8-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.int16
    :type: type

    Signed 16-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.int32
    :type: type

    Signed 32-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.int64
    :type: type

    Signed 64-bit integer. At runtime is represented as Python ``int``.
    A normal Python ``int`` will also alias to this type.

.. py:data:: cyclonedds.idl.types.uint8
    :type: type

    Unsigned 8-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.uint16
    :type: type

    Unsigned 16-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.uint32
    :type: type

    Unsigned 32-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.uint64
    :type: type

    Unsigned 64-bit integer. At runtime is represented as Python ``int``.

.. py:data:: cyclonedds.idl.types.float32
    :type: type

    Floating point type with 32-bits. At runtime is represented as Python ``float``.

.. py:data:: cyclonedds.idl.types.float64
    :type: type

    Floating point type with 64-bits. At runtime is represented as Python ``float``.
    A normal Python ``float`` will also alias to this type.

```
