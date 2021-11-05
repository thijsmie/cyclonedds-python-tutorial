from questing.quest import Quest
from cyclonedds.domain import DomainParticipant


class DomainParticipantQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="domain-participant",
            prompt="""Sail the DDS seas with a DomainParticipant

Tasks:
 * Import the `DomainParticipant` from `cyclonedds.domain` and instantiate it without arguments.
 * Pass the `DomainParticipant` to `quest.check("domain-participant", participant)`""",
            hints=[
                "The import is `from cyclonedds.domain import DomainParticipant`",
                "The instantiation is `participant = DomainParticipant()`"
            ],
            solution="""quest = journal.quest("domain-participant")
quest.prompt()
quest.start()

from cyclonedds.domain import DomainParticipant
participant = DomainParticipant()

quest.check("domain-participant", participant)
quest.finish()"""
        )
        self._checkers["domain-participant"] = self._check_participant

    def _check_participant(self, value):
        assert isinstance(value, DomainParticipant)
