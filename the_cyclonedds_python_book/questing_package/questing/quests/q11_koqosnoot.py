from questing.quest import Quest

from cyclonedds.qos import Qos, Policy, BasePolicy
from cyclonedds.util import duration

class KoqosnootQuest(Quest):
    def __init__(self, journal, seed) -> None:
        super().__init__(
            journal=journal,
            seed=seed,
            name="koqosnoot",
            prompt="""In Cyclone DDS Python the `Qos` object behaves almost like a tuple of `Policy`.
It is immutable but easy to construct. All policies are classes or singletons under the `Policy` object.
For example, "a TransientLocal Durability policy taking no arguments" would result in `Policy.Durability.TransientLocal` and
"a deadline policy of 15 seconds" would result in `Policy.Deadline(duration(seconds=15))`. To construct a `Qos` object
out of policies you simply pass them as arguments: `qos = Qos(policy1, policy2, ...)`.

Tasks:
 * Create the policies as instructed in comments and pass them to their respective checker.
""",
            hints=[
                "`policy0 = Policy.Ownership.Reliable`"
                "`policy1 = Policy.Liveliness.Automatic(duration(days=2))`"
                "`qos0 = Qos(Policy.Reliability.Reliable(duration(milliseconds=250)), Policy.History.KeepAll)`"
                """`qos1 = Qos(
    Policy.Reliability.BestEffort,
    Policy.Durability.TransientLocal,
    Policy.History.KeepAll,
    Policy.Partitions(["a", "b"])
)`""",
                "`qos2 = Qos(Policy.TransportPriority(4), base=qos1)`"
            ],
            solution="""quest = journal.quest("koqosnoot")
quest.prompt()
quest.start()

from cyclonedds.core import Qos, Policy
from cyclonedds.util import duration

# Create a Shared or Exclusive Ownership policy. They take no arguments.
# The solution is under quest.hint(index=0)
policy0 = Policy.Ownership.Shared
quest.check("policy-0", policy0)

# Create an Automatic Liveliness policy. It takes a lease duration as argument,
# make that two days. The solution is under quest.hint(index=1)
policy1 = Policy.Liveliness.Automatic(duration(days=2))
quest.check("policy-1", policy1)

# Create a Qos object with a Reliable Reliability policy, taking a max blocking
# time as argument, set that to 250 milliseconds. Also add a KeepAll History
# policy, it takes no arguments. The solution is under quest.hint(index=2)
qos0 = Qos(Policy.Reliability.Reliable(duration(milliseconds=250)), Policy.History.KeepAll)
quest.check("koqosnoot-0", qos0)

# Create any Qos object with 4 policies.
# An example solution is under quest.hint(index=3)
qos1 = Qos(
    Policy.Reliability.BestEffort,
    Policy.Durability.TransientLocal,
    Policy.History.KeepAll,
    Policy.Partition(["a", "b"])
)
quest.check("koqosnoot-1", qos1)

# Create a Qos object with 5 policies by adding one to the previous qos
# You can inherit other Qos by giving the keyword argument 'base':
#    qos = Qos(policy1, ..., base=other_qos)
# An example solution is under quest.hint(index=4)
qos2 = Qos(Policy.TransportPriority(4), base=qos1)
quest.check("koqosnoot-2", qos2)

# Example: you can inspect any QoS object by iteration
for policy in qos2:
    print(policy)

quest.finish()"""
        )
        self._checkers["policy-0"] = self._check_policy_0
        self._checkers["policy-1"] = self._check_policy_1
        self._checkers["koqosnoot-0"] = self._check_koqosnoot_0
        self._checkers["koqosnoot-1"] = self._check_koqosnoot_1
        self._checkers["koqosnoot-2"] = self._check_koqosnoot_2

    def _check_policy_0(self, value):
        assert value == Policy.Ownership.Exclusive or value == Policy.Ownership.Shared

    def _check_policy_1(self, value):
        assert value == Policy.Liveliness.Automatic(duration(days=2))

    def _check_koqosnoot_0(self, value):
        assert value == Qos(
            Policy.Reliability.Reliable(duration(milliseconds=250)),
            Policy.History.KeepAll
        )

    def _check_koqosnoot_1(self, value):
        assert isinstance(value, Qos)
        assert len(value) == 4

    def _check_koqosnoot_2(self, value):
        assert isinstance(value, Qos)
        assert len(value) == 5
