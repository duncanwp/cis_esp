FROM continuumio/miniconda3
MAINTAINER Duncan Watson-Parris <duncan.watson-parris@physics.ox.ac.uk>

ADD . /cis-esp
WORKDIR /cis-esp

RUN conda install -c conda-forge --file conda-requirements.txt
RUN pip install -r requirements.txt