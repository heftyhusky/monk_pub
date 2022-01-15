FROM continuumio/miniconda3:4.3.27
RUN apt-get update

RUN mkdir /monk_project
COPY . /monk_project/
WORKDIR /monk_project/

# install package
RUN pip install pipenv

RUN cd api && pipenv sync
RUN cd db_mission_allocate && pipenv sync