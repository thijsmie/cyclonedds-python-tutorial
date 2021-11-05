from questing.quest import Quest
from questing.types import CuriousFish, FishType
from cyclonedds.sub import DataReader
from cyclonedds.pub import DataWriter
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic


class TakenFishyStoryQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="a-fishy-story",
            prompt="""Create a `DataReader`, imported from `cyclonedds.sub` using the participant and the topic as arguments, then take a fish.

Tasks:
 * Pass the `DataReader` you created to `quest.check("fish-reader", reader)`
 * Pass the `CuriousFish` you took to `quest.check("freshly-caught", fish)`""",
            hints=[
                "The `DataReader` import is `from cyclonedds.sub import DataReader`",
                "The `DataReader` instantiation is `reader = DataReader(participant, topic)`",
                "Taking a single fish from the reader is `fish = dr.take()[0]`"
            ],
            solution="""quest = journal.quest("a-fishy-story")
quest.prompt()
quest.start()

from cyclonedds.sub import DataReader

reader = DataReader(participant, topic)
quest.check("fish-reader", reader)

fish = reader.take()[0]
quest.check("freshly-caught", fish)
quest.finish()"""
        )
        self._checkers["fish-reader"] = self._check_fish_reader
        self._checkers["freshly-caught"] = self._check_freshly_caught
        self._sample = CuriousFish(fish_type=FishType.Metallic, dorsal_fins=3, fish_name="Dee")

    def _check_fish_reader(self, value):
        assert isinstance(value, DataReader)
        dp = DomainParticipant()
        DataWriter(dp, Topic(dp, "followers", CuriousFish)).write(self._sample)

    def _check_freshly_caught(self, value):
        assert value.fish_type.value == self._sample.fish_type.value and \
               value.dorsal_fins == self._sample.dorsal_fins and \
               value.fish_name == self._sample.fish_name