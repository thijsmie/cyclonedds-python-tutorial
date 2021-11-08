FROM python:3.9.7

RUN apt-get update && \
    apt-get -y install bison cmake git && \
    apt-get purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/eclipse-cyclonedds/cyclonedds
RUN cd cyclonedds && \
    mkdir build && cd build && \
    cmake .. -DENABLE_TOPIC_DISCOVERY=ON -DENABLE_TYPE_DISCOVERY=ON && \
    cmake --build . --target install && \
    cd ../.. && rm -rf cyclonedds

ENV NB_USER cyclone
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

RUN chown -R ${NB_UID} ${HOME}
WORKDIR ${HOME}
USER ${NB_USER}
RUN echo "export PATH=${HOME}/.local/bin:/usr/local/bin:\$PATH" >> ${HOME}/.bashrc && \
    echo "export LD_LIBRARY_PATH=/usr/local/lib:\$LD_LIBRARY_PATH" >> ${HOME}/.bashrc
ENV PATH ${HOME}/.local/bin:$PATH
ENV PATH ${HOME}/.local/bin:$PATH

RUN python3 -m pip install --upgrade --user --no-cache-dir pip wheel setuptools
RUN python3 -m pip install --upgrade --user --no-cache-dir notebook jupyterhub jupyterlab \
    git+https://github.com/eclipse-cyclonedds/cyclonedds-python ipycanvas
