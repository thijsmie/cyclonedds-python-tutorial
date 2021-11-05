(install-cyclonedds-python)=
# Installation

Eclipse Cyclone DDS Python requires Python version 3.7 or higher. In the future we want to provide binary distributions from PyPi, but until those are ready you can install from source.


## Installing from source via git

To install CycloneDDS Python you will have to install [Cyclone DDS][1] first. Then set appropriate environment variables and install with pip. A full example installation of the quickest way to get started is shown below:

```bash
$ git clone https://github.com/eclipse-cyclonedds/cyclonedds
$ cd cyclonedds && mkdir build install && cd build
$ cmake .. -DCMAKE_INSTALL_PREFIX=../install
$ cmake --build . --target install
$ cd ..
$ export CYCLONEDDS_HOME="$(pwd)/install"
$ pip3 install --user git+https://github.com/eclipse-cyclonedds/cyclonedds-python
```

If you want to install with development tools add the `[dev]` component to your installation like so:

```bash
$ pip3 install --user "cyclonedds[dev] @ git+https://github.com/eclipse-cyclonedds/cyclonedds-python"
```

Installation from a local git clone:

```bash
$ cd /path/to/git/clone
$ pip3 install --user .
# or for development:
$ pip3 install --user .[dev]
# or for documentation generation
$ pip3 install --user .[docs]
```

While the quickest way to get going is the `--user` flag it is not the recommended, we recommend using [a virtual environment][2], [poetry][3], [pipenv][4] or [pyenv][5]. After the installation is complete `import cyclonedds` should now work. The `CYCLONEDDS_HOME` variable is essential for the Python backend to locate the CycloneDDS binaries so this always needs to be set when running Python code with Cyclone DDS. Have a look at the [examples](https://github.com/eclipse-cyclonedds/cyclonedds-python/examples/) to learn about how to use the Python API.


[1]: https://github.com/eclipse-cyclonedds/cyclonedds/
[2]: https://docs.python.org/3/tutorial/venv.html
[3]: https://python-poetry.org/
[4]: https://pipenv.pypa.io/en/latest/
[5]: https://github.com/pyenv/pyenv
[6]: https://docs.python.org/3/installing/index.html
