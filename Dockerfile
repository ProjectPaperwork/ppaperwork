FROM pandoc/core as pandoc_stage
FROM alpine:3.14
LABEL org.opencontainers.image.source https://github.com/ProjectPaperwork/ppaperwork

# Enable testing repository (for gosu and pandoc), update
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories
RUN apk update

# Timezone and config scripts
RUN apk add tzdata alpine-conf

# Main tools
RUN apk add python3 py3-pip py3-wheel gosu git bash libffi libffi-dev

# Documentation tools
RUN apk add doxygen graphviz

# Install pandoc from docker image
RUN apk add gmp lua5.3 lua5.3-dev
COPY --from=pandoc_stage /usr/local/bin/pandoc /usr/bin/pandoc

# Install python dependencies
RUN pip install gherkin-official
RUN pip install tabulate
RUN pip install PyYAML
RUN pip install pytz tzlocal

# Download doxygen template
RUN cd / && git clone https://github.com/jothepro/doxygen-awesome-css.git

# Setup paperwork
WORKDIR /setup
COPY . /setup/gherkin-paperwork
COPY ./img/project_logo.png /setup/project_logo.png

WORKDIR /setup/gherkin-paperwork
RUN chmod +x ./package.sh
RUN ./package.sh -i

# Setup work
COPY ./work.sh /bin/work.sh
RUN chmod +x /bin/work.sh

WORKDIR /workdir
