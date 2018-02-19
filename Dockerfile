FROM continuumio/miniconda

# to resolve the error: ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx

# update conda to latest version
RUN conda update conda

# Grab conda environment file
ADD ./environment.yml /tmp/environment.yml

# Add conda channels
RUN conda config --add channels conda-forge && \
  conda config --add channels bokeh && \
  conda config --add channels ioam && \
  conda config --add channels cball

# Install Conda packages
RUN conda env create -f /tmp/environment.yml

# do some conda magic
ENV PATH /opt/conda/envs/pyviz/bin:$PATH
ENV CONDA_DEFAULT_ENV pyviz
ENV CONDA_PREFIX /opt/conda/envs/pyviz
RUN echo $PATH
RUN conda env list

# Add our code
ADD ./apps /opt/apps
WORKDIR /opt/apps

# Expose is NOT supported by Heroku
# EXPOSE 5006

# Run the image as a non-root user
RUN adduser --disabled-login myuser
USER myuser

#
# Note: to test locally we can override the CMD by doing this in terminal.
# Then go to http://localhost:5006/webapp
#
# docker run -it -p 5006:5006 bokeh-app-uk-road-accidents-viz
#
# or
#
# docker run -it -p 5006:5006 registry.heroku.com/uk-road-accidents-viz/web
#
#

# Heroku deployment
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ "source activate pyviz && bokeh serve webapp --port=${PORT:=5006} --address=0.0.0.0" ]
