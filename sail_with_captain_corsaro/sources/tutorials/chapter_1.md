---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Chapter 1: Getting your feet wet

Welcome! This interactive tutorial teaches you the basics of DDS and the Cyclone DDS Python backend. To give it a fun spin, we will use DDS to follow along on the journey of Captain Corsaro with his ship Cyclone.

<div class="journal">
    <div class="date">June 2nd, 1674</div>
    This morning we left the harbour of Palermo, setting sail for Tunis. Weather conditions are outstanding, I hope they will hold. Getting some dry-dock time in Palermo was worth it, sailing the Cyclone with a cleaned hull for the first time in years is invigorating. It was expensive though, we need to make a capture as soon as possible.
    <div class="signature">Captain A. Corsaro</div>
</div>

All story fragments from the journal will be presented in boxes like the one above. Explanations and instructions are presented as normal text like this. Please execute the code cell below to initialize your personal copy of Captain Corsaro's journal.

```{code-cell} ipython3
from questing import Journal

journal = Journal(seed=None)
print(journal.seed)
```

## Sailing the DDS sea

DDS is a publish-subscribe based networking system that allows you to write applications that talk to eachother without worrying about shipping the bits and bytes around and retaining compatibility between platforms and programming languages. We will first explore the different entities central to a DDS system and learn how to create and use them in Python.

<div class="journal">
    <div class="date">June 7th, 1674</div>
    A dreadfull storm has blown us off course, I don't even recognize the stars anymore. We have picked a random direction counter the wind direction of the past few days and hope to find land in not too long. For now I have dubbed the waters here the DDS sea.
</div>

To join our captain on the DDS sea, or rather *DDS Domain* we use a `DomainParticipant`. A `DomainParticipant` is the central entity in any DDS application. The Domain itself is more of a virtual concept, not directly created but made up of all the participants on a network. You can have multiple domains running next to each other, identified by a *domain id*. They will remain completely separated.


The cell below retrieves the captains journal, which retrieves your quests and tracks your progress. `quest.prompt()` will display the current quest and subtasks. If you are stuck you can call `quest.hint()` to be helped along. `quest.solution()` will give you the full solution if you are really at a loss.

<hr>

> Tasks:
>  * Import the `DomainParticipant` from `cyclonedds.domain` and instantiate it without arguments.
>  * Pass the `DomainParticipant` to `quest.check("domain-participant", participant)`

```{code-cell} ipython3
from questing import Journal

journal = Journal(seed=None)
print(journal.seed)

quest = journal.quest("domain-participant")
quest.start()

# The import:

# Make participant
participant = ...

quest.check("domain-participant", participant)
quest.finish()
```

```{admonition} Click to show hint 1.
:class: toggle
The import is `from cyclonedds.domain import DomainParticipant`
```

```{admonition} Click to show hint 2.
:class: toggle
The instantiation is `participant = DomainParticipant()`
```

````{admonition} Click to show the solution.
:class: tip, toggle
```
quest = journal.quest("domain-participant")
quest.start()

from cyclonedds.domain import DomainParticipant
participant = DomainParticipant()

quest.check("domain-participant", participant)
quest.finish()
```
````

## Remaining on-topic

<div class="journal">
    <div class="date">June 8th, 1674</div>
    First Mate Boasson and I have been discussing the curious fish that jump out of the waters all around. We have observed Shimmering, Matte and Metallic looking ones with a varying number of dorsal fins. A group of them seem to be following the ship and we have taken pleasure in naming them.
</div>

In order for DDS applications to talk to each other they have to be talking about the same thing: the same `Topic`. A `Topic` in DDS consists of a *name* and a *type*. The types are usually defined using the **Object Management Group Interface Definition Language**, OMG IDL or just IDL for short. With the powerful introspection and duck-typing we don't have to rely on an IDL compiler to help us define these types, we can write Python classes directly and let Cyclone DDS Python directly generate the DDS necessities behind the scenes. If you want to learn IDL so you can interop with other languages there are other tutorials available.

You can turn Python classes into IDL structs by inheriting from `IdlStruct` from `cyclonedds.idl` and type hinting the class attributes, as if you are using [python dataclasses](https://docs.python.org/3/library/dataclasses.html). You can then implement an `__init__` method or generate one by applying `@dataclass`.


<hr>

> Create a datatype for the `CuriousFish` that has a `FishType` (Shimmering, Matte or Metallic), an integer number of dorsal fins and a string name.
> Then import `Topic` from `cyclonedds.topic` and create a `Topic` named `followers`. A `Topic` takes three arguments: a `DomainParticipant`, a name and the datatype.
>
> **Note**: your variables persist between cells, you can use the participant from the previous quest!
>
> Example datatype:
> ```python
> @dataclass
> class LogbookEntry(IdlStruct):
>     timestamp: int
>     text: str
>     author: str
>  ```
>
> Tasks:
>  * Pass the `CuriousFish` datatype to `quest.check("curious-fish", CuriousFish)`
>  * Pass the `Topic` you created to `quest.check("followers-topic", topic)`

```{code-cell} ipython3
quest = journal.quest("remain-on-topic")
quest.start()

from enum import Enum
from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

class FishType(Enum):
    Shimmering = 0
    Matte = 1
    Metallic = 2

class CuriousFish(IdlStruct):
    fish_type: FishType
    # define dorsal_fins
    # define fish_name

quest.check("curious-fish", CuriousFish)

# import

# create the topic
topic = ...

quest.check("followers-topic", topic)
quest.finish()
```

```{admonition} Click to show hint 1.
:class: toggle
The fields are `dorsal_fins: int` and `fish_name: str`.
```

```{admonition} Click to show hint 2.
:class: toggle
The topic import is `from cyclonedds.topic import Topic`.
```

```{admonition} Click to show hint 3.
:class: toggle
The topic instantiation is `topic = Topic(participant, "followers", CuriousFish)`
```

````{admonition} Click to show the solution.
:class: tip, toggle
```
quest = journal.quest("remain-on-topic")
quest.start()

from enum import Enum
from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

class FishType(Enum):
    Shimmering = 0
    Matte = 1
    Metallic = 2

@dataclass
class CuriousFish(IdlStruct):
    fish_type: FishType
    dorsal_fins: int
    fish_name: str

quest.check("curious-fish", CuriousFish)

from cyclonedds.topic import Topic
topic = Topic(participant, "follower_fish", CuriousFish)

quest.check("followers-topic", topic)
quest.finish()
```
````

## Taken, a fishy story

<div class="journal">
    <div class="date">June 12th, 1674</div>
    One of the crew finally managed to catch a fish, hopefully we can catch more so we can stretch our food supplies. We have been sailing for five days now without seeing any land or other ship. Are we going the right direction or are we doomed to sail the endless oceans?
</div>

We will now finally interact with the DDS system. By subscribing to the `follower-fish` topic and `taking` a sample we will discover what the fish our captain talked about actually looked like. This is done through `Subscribers` and `DataReaders`. We will disregard the `Subscriber` for now and only work with a `DataReader`. It has several reading and taking methods that allow you to receive data from the network. They are `read`, `take`, `read_next`, `take_next`, `read_iter`, `take_iter`, `read_aiter` and `take_aiter`. We will stick with a simple `take` for now, which gives you a list of available samples. A *sample* is simply an instance of the datatype of the `Topic`.

<hr>

> Create a `DataReader`, imported from `cyclonedds.sub` using the participant and the topic as arguments, then take a fish.
>
> Tasks:
>  * Pass the `DataReader` you created to `quest.check("fish-reader", reader)`
>  * Pass the `CuriousFish` you took to `quest.check("freshly-caught", fish)`

```{code-cell} ipython3
quest = journal.quest("a-fishy-story")
quest.start()

# The import

# Create the reader
reader = ...
quest.check("fish-reader", reader)

# Take the fish
fish = ...
print(fish)

quest.check("freshly-caught", fish)
quest.finish()
```

```{admonition} Click to show hint 1.
:class: toggle
The `DataReader` import is `from cyclonedds.sub import DataReader`
```

```{admonition} Click to show hint 2.
:class: toggle
The `DataReader` instantiation is `reader = DataReader(participant, topic)`
```

```{admonition} Click to show hint 3.
:class: toggle
Taking a single fish from the reader is `fish = dr.take()[0]`
```

````{admonition} Click to show the solution.
:class: tip, toggle
```
quest = journal.quest("a-fishy-story")
quest.start()

from cyclonedds.sub import DataReader

reader = DataReader(participant, topic)
quest.check("fish-reader", reader)

fish = reader.take()[0]
quest.check("freshly-caught", fish)
quest.finish()
```
````