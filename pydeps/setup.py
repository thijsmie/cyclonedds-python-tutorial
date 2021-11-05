from skbuild import setup
import os
import sys


os.environ['CYCLONEDDS_HOME'] = sys.path[-1] + "/cyclonedds"
os.environ['CMAKE_PREFIX_PATH'] = sys.path[-1] + "/cyclonedds"
print(sys.path)


# Setup magic
setup(
    name='cyclone-book',
    version='0.0.1',
    description='Eclipse Cyclone DDS installer via Python',
    author='Eclipse Cyclone DDS Committers',
    maintainer='Thijs Miedema',
    maintainer_email='thijs.miedema@adlinktech.com',
    python_requires='>=3.6',
    zip_safe=False,
    license="EPL-2.0, BSD-3-Clause",
    install_requires=[
        'jupyter-book',
        'matplotlib',
        'numpy',
        'cyclonedds @ git+https://github.com/thijsmie/cyclonedds-python'
    ],
    cmake_source_dir='cyclone'
)