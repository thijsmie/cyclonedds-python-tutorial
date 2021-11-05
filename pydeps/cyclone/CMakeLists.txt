cmake_minimum_required(VERSION 3.10)
project(AutoCycloneDDS)

include(ExternalProject)

ExternalProject_Add(CycloneDDS
    GIT_REPOSITORY https://github.com/eclipse-cyclonedds/cyclonedds
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/cyclonedds -DENABLE_TOPIC_DISCOVERY=ON -DENABLE_TYPE_DISCOVERY=ON -DENABLE_SSH=OFF -DENABLE_SECURITY=OFF
)

install(DIRECTORY ${CMAKE_BINARY_DIR}/cyclonedds DESTINATION ".")
get_filename_component(CY_HOME "." ABSOLUTE)
set(ENV{CYCLONEDDS_HOME} $CY_HOME)
