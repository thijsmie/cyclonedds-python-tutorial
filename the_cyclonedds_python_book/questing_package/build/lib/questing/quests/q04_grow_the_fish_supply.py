from questing.quest import Quest
from questing.types import CuriousFish, FishType
from cyclonedds.sub import DataReader
from cyclonedds.pub import DataWriter
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic


class GrowTheFishSupplyQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="grow-the-fish-supply",
            prompt="""Create a `DataWriter`, imported from `cyclonedds.pub` using the participant and the topic as arguments, then write a `CuriousFish`.

Tasks:
 * Pass the `DataWriter` you created to `quest.check("fish-writer", writer)`
 * Write a `CuriousFish` with parameters of your choosing.
""",
            hints=[
                "The `DataWriter` import is `from cyclonedds.pub import DataWriter`."
                "The `DataWriter` instantiation is `writer = DataWriter(participant, topic)`."
                "Instantiating a fish can be done like this: `fish = CuriousFish(fish_type=FishType.Matte, dorsal_fins=6, fish_name=\"Harry\")`."
                "Writing a fish can be done like this: `writer.write(fish)`."
            ],
            solution="""quest = journal.quest("grow-the-fish-supply")
quest.prompt()
quest.start()

from cyclonedds.pub import DataWriter

writer = DataWriter(participant, topic)
quest.check("fish-writer", writer)

fish = CuriousFish(fish_type=FishType.Matte, dorsal_fins=6, fish_name="Harry")
writer.write(fish)

quest.finish()"""
        )
        self._checkers["fish-writer"] = self._check_fish_writer
        self._reader = None

    def start(self):
        self._reader = None
        super().start()

    def _check_fish_writer(self, value):
        assert isinstance(value, DataWriter)
        dp = DomainParticipant()
        self._reader = DataReader(dp, Topic(dp, "followers", CuriousFish))

    def _pre_finish(self):
        assert self._reader.read()
