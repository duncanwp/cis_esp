FROM continuumio/miniconda3
MAINTAINER Duncan Watson-Parris <duncan.watson-parris@physics.ox.ac.uk>

RUN conda install -c conda-forge --file conda-requirements.txt
RUN pip install --file requirements.txt