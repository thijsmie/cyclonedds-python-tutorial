from questing.quest import Quest
from cyclonedds.topic import Topic

from dataclasses import is_dataclass, fields


class RemainOnTopicQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="remain-on-topic",
            prompt="""Create a datatype for the `CuriousFish` that has a `FishType` (Shimmering, Matte or Metallic), an integer number of dorsal fins and a string name.
Then import `Topic` from `cyclonedds.topic` and create a `Topic` named `followers`. A `Topic` takes three arguments: a `DomainParticipant`, a name and the datatype.

**Note**: your variables persist between cells, you can use the participant from the previous quest!

Example datatype:
```python
@dataclass
class LogbookEntry(IdlStruct):
    timestamp: int
    text: str
    author: str
```

Tasks:
 * Pass the `CuriousFish` datatype to `quest.check("curious-fish", CuriousFish)`
 * Pass the `Topic` you created to `quest.check("followers-topic", topic)`""",
            hints=[
                "The fields are `dorsal_fins: int` and `fish_name: str`",
                "The topic import is `from cyclonedds.topic import Topic`",
                "The topic instantiation is `topic = Topic(participant, \"followers\", CuriousFish)`"
            ],
            solution="""quest = journal.quest("remain-on-topic")
quest.prompt()
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
quest.finish()"""
        )
        self._checkers["curious-fish"] = self._check_curious_fish
        self._checkers["followers-topic"] = self._check_followers_topic

    def _check_curious_fish(self, value):
        assert is_dataclass(value)
        fields_ = fields(value)
        assert fields_[0].type.Shimmering.value == 0
        assert fields_[0].type.Matte.value == 1
        assert fields_[0].type.Metallic.value == 2
        assert fields_[1].type == int
        assert fields_[2].type == str

    def _check_followers_topic(self, value):
        assert isinstance(value, Topic)
        assert value.typename == "__main__::CuriousFish"
        assert value.name == "followers"