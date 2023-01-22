# using ubuntu LTS version
FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/annotator-user/bio_annotator/venv
ENV PATH="/home/annotator-user/bio_annotator/venv/bin:$PATH"
ENV VIRTUAL_ENV=/home/annotator-user/bio_annotator/venv
# install requirements
COPY poetry.lock .
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry install

FROM annotation/nirvana:3.14 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*


RUN useradd --create-home annotator-user
RUN mkdir /home/annotator-user/bio_annotator/
COPY --from=builder-image /home/annotator-user/bio_annotator/venv /home/annotator-user/bio_annotator/venv

USER annotator-user
WORKDIR /home/annotator-user/bio_annotator
COPY ./bio_annotator/. /home/annotator-user/bio_annotator/

EXPOSE 5000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/annotator-user/bio_annotator/venv
ENV PATH="/home/annotator-user/bio_annotator/venv/bin:$PATH"
ENV NIRVANA_EXC="dotnet"
ENV NIRVANA_DATA="/scratch"
ENV NIRVANA_BIN="/opt/nirvana/Nirvana.dll"
# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
CMD ["gunicorn","-b", "0.0.0.0:5000", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--worker-tmp-dir", "/dev/shm", "--chdir", "/home/annotator-user/", "server:app"]