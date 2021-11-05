#!/usr/bin/env python
"""
 * Copyright(c) 2021 ADLINK Technology Limited and others
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0, or the Eclipse Distribution License
 * v. 1.0 which is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * SPDX-License-Identifier: EPL-2.0 OR BSD-3-Clause
"""

import re
from pathlib import Path
from skbuild import setup


this_directory = Path(__file__).resolve().parent
# invalidate cmake cache
for cache_file in (this_directory / "_skbuild").rglob("CMakeCache.txt"):
    cache_file.write_text(
        re.sub("^//.*$\n^[^#].*pip-build-env.*$", "", cache_file.read_text(), flags=re.M)
    )


setup(
    name='cyclone',
    version='0.0.1',
    description='Eclipse Cyclone DDS installer via Python',
    author='Eclipse Cyclone DDS Committers',
    maintainer='Thijs Miedema',
    maintainer_email='thijs.miedema@adlinktech.com',
    python_requires='>=3.6',
    zip_safe=False,
    license="EPL-2.0, BSD-3-Clause"
)
