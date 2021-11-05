(tool-ddsls)=
# ddsls

When using DDS, it's sometimes useful to know what DDS entities are
running in the system. The [**ddsls**][1] is a tool that subscribes to the
Built-in topics, and shows the information of the domain participants,
data readers and data writers in the system.

## Usage

To run the **ddsls**, you can use:

``` console
$ ddsls [Options]
```

You can view what options you have with the **ddsls** by using the
command:

``` console
$ ddsls --help
```

And the help message is as follows:

``` console
usage: ddsls [-h] [-i ID] [-f FILENAME] [-j] [-w] [-v] [-r RUNTIME] (-a | -t {dcpsparticipant,dcpssubscription,dcpspublication})

optional arguments:
-h, --help            show this help message and exit
-i ID, --id ID        Define the domain participant id
-f FILENAME, --filename FILENAME
                      Write results to file in JSON format
-j, --json            Print output in JSON format
-w, --watch           Watch for data reader & writer & qoses changes
-v, --verbose         View the sample when Qos changes
-r RUNTIME, --runtime RUNTIME
                      Limit the runtime of the tool, in seconds.
-a, --all             for all topics
-t {dcpsparticipant,dcpssubscription,dcpspublication}, --topic {dcpsparticipant,dcpssubscription,dcpspublication}
                      for one specific topic
```

There are several options you can choose to use the **ddsls** according
to your needs, which will be further explained in the following
sections.

For checking the DDS entity information, you can use the `--topic` or
`--all` option to specify which entity's information you want to see,
the `--id` option to define which domain you like to check using the id
of the domain participant, the `--watch` option to monitor the changes
in the system as entities being created and disposed.

For viewing options, you can use the `--json` option to view the output
data in JSON format, the `--verbose` option to view the full sample
information when the entity's QoS changes.

For additional options, you can use the `--filename` option to define
the name of file you want to output the result to, the `--runtime`
option to specify how long the **ddsls** will run.

### Topic

To use the **ddsls**, you need to specify the topic you're subscribing
to using the `--topic` or `--all` option.

For `--topic` option, you can choose from `dcpsparticipant`,
`dcpssubscription` and `dcpspublication`.

The `dcpsparticipant`, `dcpssubscription` and `dcpspublication`
subscribes to the **BuiltinTopicDcpsParticipant**,
**BuiltinTopicSubscription** and **BuiltinTopicDcpsPublication** topic
respectively, and will show the information of all the participants,
subscribers and publishers

[1]: https://github.com/eclipse-cyclonedds/cyclonedds-python/tree/master/src/cyclonedds/cyclonedds/tools/ddsls