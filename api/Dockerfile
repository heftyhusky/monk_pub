FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /monk_project
COPY . /monk_project/
WORKDIR /monk_project/

# install package
RUN pip install pipenv && pipenv sync

# genenv
RUN VERSION=DEFAULT python genenv.py
 
# 預設執行的指令
CMD ["pipenv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]
