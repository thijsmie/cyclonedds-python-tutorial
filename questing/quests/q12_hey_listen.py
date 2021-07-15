from questing.quest import Quest
from questing.types import Wave

from cyclonedds.qos import Qos, Policy, BasePolicy
from cyclonedds.util import duration
from cyclonedds.sub import DataReader
from cyclonedds.domain import DomainParticipant
from cyclonedds.pub import DataWriter
from cyclonedds.topic import Topic


from threading import Thread
from dataclasses import is_dataclass, fields
from time import sleep
from random import Random



class HeyListenQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="hey-listen",
            prompt="""
Tasks:
 * Create a `Wave` datatype and topic. A wave has a `height` as integer (centimeters) and a `volume` as float (decibels).
    * Check the `Wave` datatype with `quest.check("wave", Wave)`
 * Import `Listener` from `cyclonedds.core` and create a `MyListener` subclass that sets a `threading.Event` when data is available.
    * `on_data_available` receives one extra argument: the reader that has data available. Since we have only one reader you can ignore the argument,
      but your function should be able to receive it.
 * Instantiate the listener, create a DataReader for your topic while attaching the listener and a qos object with a Reliable Reliability policy.
    * max_blocking_time is only relevant on the DataWriter side, just set it to something.
    * You can add a listener to any entity with a constructor keyword argument `listener=mylistener` argument
    * You can add a qos to any entity with a constructor keyword argument `qos=myqos` argument
    * Check the reader with `quest.check("reader", reader)`
 * Wait for the `threading.Event` to fire and read the wave samples iteratively from the datareader
    * All samples are passed to `quest.check("a-lovely-wave", wave)
""",
            hints=[
                "The `Wave` datatype looks as follows: ```python\n@cdr\nclass Wave:\n\theight: int\n\tvolume: float\n\n```",
                "'MyListener' is defined as follows: ```python\nevent = Event()\nclass MyListener(Listener):\n\tdef on_data_available(self, reader):\n\t\tevent.set()\n```"
                "`myqos` is defined as `Qos(Policy.Reliability.Reliable(duration(milliseconds=200)))`",
                "`reader` is defined as `DataReader(participant, topic, qos=myqos, listener=mylistener)`"],
            solution="""quest = journal.quest("hey-listen")
quest.prompt()
quest.start()

from pycdr import cdr
from cyclonedds.core import Listener, Qos, Policy
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.util import duration
from threading import Event

@cdr
class Wave:
    height: int
    loudness: float

quest.check("wave", Wave)

event = Event()
class MyListener(Listener):
    def on_data_available(self, reader):
        event.set()

participant = DomainParticipant()
topic = Topic(participant, "Wave", Wave)
mylistener = MyListener()
myqos = Qos(Policy.Reliability.Reliable(duration(milliseconds=200)))
reader = DataReader(participant, topic, qos=myqos, listener=mylistener)
quest.check("reader", reader)

event.wait()

for wave in reader.read_iter(timeout=duration(milliseconds=200)):
    print(wave)
    quest.check("a-lovely-wave", wave)

quest.finish()"""
        )
        self._checkers["wave"] = self._check_wave
        self._checkers["reader"] = self._check_reader
        self._checkers["a-lovely-wave"] = self._check_a_lovely_wave
        self._thread = None

    def _check_wave(self, value):
        assert is_dataclass(value)
        fields_ = fields(value)
        assert len(fields_) == 2
        assert fields_[0].type == int
        assert fields_[1].type == float
        self._user_height_field = fields_[0].name
        self._user_volume_field = fields_[1].name

    def _check_reader(self, value):
        assert isinstance(value, DataReader)
        assert value.topic.typename == "__main__::Wave"
        assert value.topic.name == "Wave"
        assert Policy.Reliability.Reliable in value.get_qos()
        random = Random(self._seed)
        self._samples = [Wave(height=random.randint(100, 200), volume=40 + 30 * random.random()) for i in range(10)]
        self._dp = DomainParticipant()
        self._topic = Topic(self._dp, "Wave", Wave)
        self._thread = Thread(target=self._pubwaves)
        self._thread.start()
        self._recv = 0

    def _pubwaves(self):
        sleep(0.4)
        dw = DataWriter(self._dp, self._topic, qos=Qos(Policy.Reliability.Reliable(duration(milliseconds=500))))
        for s in self._samples:
            dw.write(s)
            sleep(0.01)

    def _check_a_lovely_wave(self, value):
        assert getattr(value, self._user_height_field) == self._samples[self._recv].height
        assert getattr(value, self._user_volume_field) == self._samples[self._recv].volume
        self._recv += 1

    def finish(self, no_out=False):
        if self._thread:
            self._thread.join()
            self._thread = None
        super().finish(no_out)
