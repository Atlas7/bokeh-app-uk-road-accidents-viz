FROM heroku/miniconda

# Grab requirements.txt.
# ADD ./requirements.txt /tmp/requirements.txt

# Install pip dependencies
# RUN pip install -qr /tmp/requirements.txt

# Grab conda environment file
# ADD ./environment.yml /tmp/environment.yml

# Install Conda packages
# RUN conda env create -f /tmp/environment.yml

# Add conda channels
conda config --add channels cball ioam bokeh conda-forge

# Install conda packages
conda install -n py36_env "notebook>=5.1" \
 holoviews geoviews pandas xarray datashader \
 paramnb parambokeh "bokeh=0.12.10" networkx \
 "streamz=0.2.0" "dask=0.15.4" geopandas scikit-image \
 selenium phantomjs fastparquet pytest>=3.2 python-snappy \
 "ipywidgets>=6,<7" cffi

# Add our code
ADD ./apps /opt/apps
WORKDIR /opt/apps

CMD bokeh serve webapp --port=$PORT --host=uk-road-accidents-viz.herokuapp.com --host=* --address=0.0.0.0 --use-xheaders