FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# install ngspice
RUN apt-get update && sudo apt-get -y install ngspice

# intstall my Python modules
COPY requirements.txt /tmp
WORKDIR /tmp
RUN python3 -m pip install -r requirements.txt


# RUN pip install ipykernel==6.29.0
# RUN pip install ipywidgets==8.1.1
# RUN pip install numpy==1.26.3
# RUN pip install matplotlib==3.8.2
# RUN pip install scipy==1.12.0
# RUN pip install isort==5.13.2
