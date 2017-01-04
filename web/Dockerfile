FROM continuumio/miniconda3
MAINTAINER Duncan Watson-Parris <duncan.watson-parris@physics.ox.ac.uk>

WORKDIR /cis-esp

# Add then install the conda requirements - this can then be cached
ADD ./conda-requirements.txt /cis-esp/conda-requirements.txt
RUN conda install -c conda-forge --file conda-requirements.txt

# Add then install the pip requirements - this can then be cached
ADD ./requirements.txt /cis-esp/requirements.txt
RUN pip install -r requirements.txt

# Add all the project code
ADD . /cis-esp

RUN mkdir media logs
VOLUME ["/cis-esp/media/", "/cis-esp/logs/"]

# Port to expose
EXPOSE 80

ENTRYPOINT ["/cis-esp/docker-entrypoint.sh"]