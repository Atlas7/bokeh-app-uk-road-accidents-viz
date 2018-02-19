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

# Add our code
ADD ./apps /opt/apps
WORKDIR /opt/apps

# Expose is NOT supported by Heroku
# EXPOSE 8080

# Run the image as a non-root user
RUN adduser --disabled-login myuser
USER myuser

# Note: to test locally we can override the CMD by doing this in terminal.
# Then go to http://localhost:5006/webapp
#
# export PORT=5006 && docker run -i -t -p $PORT:$PORT bokeh-app-uk-road-accidents-viz:miniconda-pyviz-1 /bin/bash -c "source activate pyviz && bokeh serve webapp --port=$PORT --address=0.0.0.0 --use-xheaders"
# or
# export PORT=5006 && docker run -i -t -p $PORT:$PORT bokeh-app-uk-road-accidents-viz:miniconda-pyviz-1
# or
# export PORT=5006 && docker run -i -t -p $PORT:$PORT registry.heroku.com/uk-road-accidents-viz/web /bin/bash -c "source activate pyviz && bokeh serve webapp --port=$PORT --address=0.0.0.0 --use-xheaders"
#
# Heroku deployment
#CMD [ "source activate pyviz && bokeh serve webapp --port=$PORT --address=0.0.0.0 --use-xheaders --host=uk-road-accidents-viz.herokuapp.com" ]

CMD [ "source activate pyviz && bokeh serve webapp --port=$PORT --address=0.0.0.0 --use-xheaders" ]
