# cyclonedds.builtin

The `builtin` module contains the tools to subscribe to the Built-in Topics. This allows you to receive information on what is happening inside the DDS network.

**Note:** If you want `BuiltinTopicDcpsTopic` to work Cyclone DDS should be built with option `-DENABLE_TOPIC_DISCOVERY`.


```{eval-rst}

.. autoclass:: cyclonedds.builtin.BuiltinDataReader
   :members:
   :show-inheritance:

   .. automethod:: __init__

.. autoclass:: cyclonedds.builtin.DcpsParticipant
   :members:
   :exclude-members: struct_class

.. autoclass:: cyclonedds.builtin.DcpsEndpoint
   :members:
   :exclude-members: struct_class

.. autoclass:: cyclonedds.builtin.BuiltinTopic
   :members:
   :show-inheritance:

.. autodata:: cyclonedds.builtin.BuiltinTopicDcpsParticipant
   :annotation:

.. autodata:: cyclonedds.builtin.BuiltinTopicDcpsTopic
   :annotation:

.. autodata:: cyclonedds.builtin.BuiltinTopicDcpsPublication
   :annotation:

.. autodata:: cyclonedds.builtin.BuiltinTopicDcpsSubscription
   :annotation:

```
