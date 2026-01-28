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

# RUN apt-get update
# RUN apt-get update

# Copy in the SDK
COPY --from=kbase/kb-sdk:1.2.1 /src /sdk
RUN sed -i 's|/src|/sdk|g' /sdk/bin/*


# Fix KBase Catalog Registration Issue
ENV PIP_PROGRESS_BAR=off


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

# RUN make all

RUN /opt/conda/bin/pip install -r /kb/module/requirements_kbase.txt

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
