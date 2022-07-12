FROM ubuntu:22.04

#
LABEL org.opencontainers.image.source https://github.com/ProjectPaperwork/ppaperwork

#
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    cmake \
    build-essential \
    python3-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    flex bison \
    graphviz \
    python3-pip \
    pandoc \
    doxygen

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gosu

RUN pip install gherkin-official
RUN pip install tabulate
RUN pip install PyYAML

RUN cd / && git clone https://github.com/jothepro/doxygen-awesome-css.git

#
WORKDIR /setup
COPY . /setup/gherkin-paperwork
WORKDIR /setup/gherkin-paperwork
RUN chmod +x ./package.sh
RUN ./package.sh -i

#
WORKDIR /workdir

COPY ./container-entrypoint /container-entrypoint
RUN chmod +x /container-entrypoint
ENTRYPOINT [ "/container-entrypoint" ]

