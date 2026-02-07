FROM oschwengers/bakta:v1.11.4
# FROM kbase/sdkpython:3.8.10
LABEL maintainer=fliu@anl.gov
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.
RUN export TZ=Etc/UTC
RUN export DEBIAN_FRONTEND=noninteractive

RUN apk add build-base
RUN apk add openjdk8-jre
# RUN apt-get update

# Copy in the SDK
COPY --from=kbase/kb-sdk:1.2.1 /src /sdk
RUN sed -i 's|/src|/sdk|g' /sdk/bin/*

ENV PATH=/sdk/bin:$PATH

# Fix KBase Catalog Registration Issue
ENV PIP_PROGRESS_BAR=off

# Add KBase deps
COPY requirements_kbase.txt /tmp/requirements_kbase.txt
RUN /opt/conda/bin/pip install -r /tmp/requirements_kbase.txt
ADD biokbase /opt/conda/lib/python3.11/site-packages
ADD biokbase/user-env.sh /kb/deployment/user-env.sh


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN PATH=/sdk/bin:$PATH make all



ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
