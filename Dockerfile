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

# Note: to test locally at http://localhost:5006/webapp, we can either:
#
# option 1: build container and do a docker run (build it yourself locally):
# $ docker build -t bokeh-app-uk-road-accidents-viz .
# $ docker run -i -t -p 5006:5006 bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"
#
# option 2: use the one on dockerhub (built by github user: atlas7)
# $ docker run -i -t -p 5006:5006 atlas7/bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"
#
# option 3: use the one on Heroku Container Registory (built by github user: atlas7)
# $ docker run -i -t -p 5006:5006 registry.heroku.com/uk-road-accidents-viz/web "bokeh serve webapp --port=5006 --address=0.0.0.0"
#

# Heroku deployment
# Note: if you were to deploy this app yourself to say, Heroku, simply replace the host arguments with your Heroku app host name.
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD bokeh serve webapp --port=${PORT} --address=0.0.0.0 --host=uk-road-accidents-viz.herokuapp.com --host=desolate-dusk-31283.herokuapp.com
