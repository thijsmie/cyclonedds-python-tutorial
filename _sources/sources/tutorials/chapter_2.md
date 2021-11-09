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

# Chapter 2: A Beach Holiday?

<div class="journal">
    <div class="date">June 20th, 1674</div>
    <p>Today we made landing on the first island, which I have dubbed Partecipante. Small but plentiful in coconuts, dry wood and root vegetables. The presence of coconuts on this island without any proof of human intervention tells me we are definitely not in the mediterranean anymore, if that wasn't clear from the days travel without land in sight before.</p>
    <p>One of the Dutch crewmates was commenting on the different coconut palm variaties, apparantly amazed by the great local variety in "koQoSnoten".</p>
    <div class="signature">Captain A. Corsaro</div>
</div>

This is chapter 2 of the Cyclone DDS Python tutorial, where we will dive into Qos, Listeners and WaitSets. The basics of topics, readers and writers were explained in chapter 1 and you can always go back to it.

Turn the journal to chapter 2:

```{code-cell} python
from questing import Journal

journal = Journal(seed=None)
print(journal.seed)
```

## koQoSnoten

QoS stands for Quality of Service. In DDS you can apply a set of QoS policies to any entity, controlling the behaviour of the DDS system. DDS cannot know which data is critically important and which is actually irrelevant after a few seconds, so QoS allows you to tell DDS the meta-data around data delivery, lifetime and storage. All policies on the writer and reader side together form the "contract" that DDS will have to furfill. Here some user discretion is adviced: it is possible to cause incompatibilities between reader and writer with some of the QoS policies, creating a contract that is impossible for DDS to furfill.

<hr>

> In Cyclone DDS Python the `Qos` object behaves almost like a tuple of `Policy`.
> It is immutable but easy to construct. All policies are classes or singletons under the `Policy` object.
> For example, "a TransientLocal Durability policy taking no arguments" would result in `Policy.Durability.TransientLocal` and
> "a deadline policy of 15 seconds" would result in `Policy.Deadline(duration(seconds=15))`. To construct a `Qos` object
> out of policies you simply pass them as arguments: `qos = Qos(policy1, policy2, ...)`.
>
> Tasks:
>  * Create the policies as instructed in comments and pass them to their respective checker.

```{code-cell} python
quest = journal.quest("koqosnoot")
quest.start()

from cyclonedds.core import Qos, Policy
from cyclonedds.util import duration

# Create a Shared or Exclusive Ownership policy. They take no arguments.
# The solution is under hint 1.
policy0 = None
quest.check("policy-0", policy0)

# Create an Automatic Liveliness policy. It takes a lease duration as argument,
# make that two days. The solution is under hint 2.
policy1 = None
quest.check("policy-1", policy1)

# Create a Qos object with a Reliable Reliability policy, taking a max blocking
# time as argument, set that to 250 milliseconds. Also add a KeepAll History
# policy, it takes no arguments. The solution is under hint 3.
qos0 = None
quest.check("koqosnoot-0", qos0)

# Create any Qos object with 4 policies.
# An example solution is under hint 4.
qos1 = None
quest.check("koqosnoot-1", qos1)

# Create a Qos object with 5 policies by adding one to the previous qos
# You can inherit other Qos by giving the keyword argument 'base':
#    qos = Qos(policy1, ..., base=other_qos)
# An example solution is under hint 5.
qos2 = None
quest.check("koqosnoot-2", qos2)

# Example: you can inspect any QoS object by iteration
# for policy in qos2:
#    print(policy)

quest.finish()
```


````{admonition} Click to show hint 1.
:class: toggle
```python
policy0 = Policy.Ownership.Reliable
```
````

````{admonition} Click to show hint 2.
:class: toggle
```python
policy1 = Policy.Liveliness.Automatic(duration(days=2))
```
````

````{admonition} Click to show hint 3.
:class: toggle
```python
qos0 = Qos(Policy.Reliability.Reliable(duration(milliseconds=250)), Policy.History.KeepAll)
```
````

````{admonition} Click to show hint 4.
:class: toggle
```python
qos1 = Qos(
    Policy.Reliability.BestEffort,
    Policy.Durability.TransientLocal,
    Policy.History.KeepAll,
    Policy.Partitions(["a", "b"])
)
```
````

````{admonition} Click to show hint 5.
:class: toggle
```python
qos2 = Qos(Policy.TransportPriority(4), base=qos1)
```
````

````{admonition} Click to show the solution.
:class: tip, toggle
```python
quest = journal.quest("koqosnoot")
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

quest.finish()
```
````
