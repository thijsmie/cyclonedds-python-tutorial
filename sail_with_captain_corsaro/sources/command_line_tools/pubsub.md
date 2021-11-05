(tool-pubsub)=
# pubsub

When using DDS, it's sometimes useful to do some manual testing,
publishing and subscribing to specific topics. [**pubsub**][1] is the tool
for that.

For now, the **pubsub** can be used to read/write to a user-defined
topic with customized QoS, and you can do the read/write by simply
typing what to publish.

In the future, with the support of XTypes, the **pubsub** will also be
able to read/write to arbitrary topic that exists in the system. This
way, you will be able to use the **pubsub** to read/write to any topics
in the system.

## Usage

To use the **pubsub**, you can use:

``` console
$ pubsub [Options]
```

You can view what options you have with the **pubsub** by using the
command:

``` console
$ pubsub --help
```

And the help message is as follows:

``` console
usage: pubsub [-h] [-T TOPIC] [-f FILENAME] [-eqos {all,topic,publisher,subscriber,datawriter,datareader}] [-q QOS [QOS ...]] [-r RUNTIME] [--qoshelp]

optional arguments:
-h, --help              show this help message and exit
-T TOPIC, --topic TOPIC
                        The name of the topic to publish/subscribe to
-f FILENAME, --filename FILENAME
                        Write results to file in JSON format
-eqos {all,topic,publisher,subscriber,datawriter,datareader}, --entityqos {all,topic,publisher,subscriber,datawriter,datareader}
                        Select the entites to set the qos.
                        Choose between all entities, topic, publisher, subscriber, datawriter and datareader. (default: all).
                        Inapplicable qos will be ignored.
-q QOS [QOS ...], --qos QOS [QOS ...]
                        Set QoS for entities, check '--qoshelp' for available QoS and usage
-r RUNTIME, --runtime RUNTIME
                        Limit the runtime of the tool, in seconds.
--qoshelp               e.g.:
                            --qos Durability.TransientLocal
                            --qos History.KeepLast 10
                            --qos ReaderDataLifecycle 10, 20
                            --qos Partition [a, b, 123]
                            --qos PresentationAccessScope.Instance False, True
                            --qos DurabilityService 1000, History.KeepLast 10, 100, 10, 10
                            --qos Durability.TransientLocal History.KeepLast 10

                        Available QoS and usage are:
                        --qos Reliability.BestEffort
                        --qos Reliability.Reliable [max_blocking_time<integer>]
                        --qos Durability.Volatile
                        --qos Durability.TransientLocal
                        --qos
```

[1]: https://github.com/eclipse-cyclonedds/cyclonedds-python/tree/master/src/cyclonedds/cyclonedds/tools/pubsub