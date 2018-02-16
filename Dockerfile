FROM heroku/miniconda

# Grab requirements.txt.
# ADD ./requirements.txt /tmp/requirements.txt

# Install pip dependencies
# RUN pip install -qr /tmp/requirements.txt

# Grab conda environment file
ADD ./environment.yml /tmp/environment.yml

# Install Conda packages
RUN conda env create -f /tmp/environment.yml

# Add our code
ADD . /opt/webapp
WORKDIR /opt/webapp

CMD source activate pyviz && bokeh serve /opt/webapp/app --port=$PORT --host=uk-road-accidents-viz.herokuapp.com --host=* --address=0.0.0.0 --use-xheaders