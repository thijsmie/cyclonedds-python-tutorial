# built from docker-base, do it this way to speed up binder launch
FROM thijsmie/eclipse-cyclonedds-python-docker-base:test-3

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

RUN python3 -m pip install --user --upgrade --no-cache-dir ./questing_package
