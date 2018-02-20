"""
Bokeh Web Application for Big Data Visualization - with HoloViews and Datashader
===

MIT License

Copyright (c) 2018 Johnny Chan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import path
import pandas as pd
import dask.dataframe as dd
import holoviews as hv
import geoviews as gv
import cartopy.crs as crs
from holoviews.operation.datashader import aggregate, datashade, dynspread, shade
from datashader.colors import Hot
# from colorcet import cm_n, fire
from bokeh.models import WMTSTileSource
from bokeh.tile_providers import STAMEN_TERRAIN, STAMEN_TONER
# from bokeh.io import curdoc
from utils import cm, get_plot_params
# from hv.streams import RangeXY
import warnings

# Ignore the excessive repeated warnings. Comment this out if you want warnings.
warnings.filterwarnings("ignore")

# Use Bokeh Backend for HoloViews
hv.extension('bokeh')

# Get absolute path of this file - I've stolen this code from download_sample_data.py
here = path.abspath(path.join(path.split(__file__)[0]))
accidents_file = path.join(here, 'data/dftRoadSafety_Accidents_2016_tiny.pkl')

# Adjust dynspread parameters so our zoomed-in data points don't look too tiny
dynspread.max_px=30
dynspread.threshold=0.4

# Width of each plot in Pixel. (Height will be auto-computed to maintain aspect ratio)
PLOT_WIDTH = 600

# Load data and Datashade it (load Pandas dataframe and convert it to a Dask DataFrame)
df1 = pd.read_pickle(accidents_file)
# df1 = pd.read_pickle('./data/dftRoadSafety_Accidents_2016_tiny.pkl')
ddf = dd.from_pandas(df1, npartitions=1).persist()

# We will only need the Dask DataFrame from now on. So let's delete the Pandas DataFrame.
# TODO: potential opportunity to just use Dask and skip Pandas altogether.
del df1

# Depoint a HoloViews Element. Essentially all the Web Mercator Coordinates on a 2D surface
points = hv.Points(ddf, kdims=['webm_x', 'webm_y'])

# Define some bounding boxes in a tuple of Longitude Range (westmost, eastmost), Latitude Range (southmost, northmost)
bboxes = {
    "gb": ((-15.381, 7.251), (48.749, 61.502)),
    "gb_mainland": ( (-12.129, 5.120), (49.710, 58.745)),
    "gb_long": ((-8.745, 2.241), (48.749, 61.502)),
    "gb_wide": ((-21.709, 15.293), (48.749, 61.502)),
    "london": ((-0.643, 0.434), (51.200, 51.761)),
    "london_2": ((-0.1696, 0.0130), (51.4546, 51.5519)),
    "london_3": ((-0.1330, -0.0235), (51.4741, 51.5322)),
    "manchester": ((-3.049, -1.505), (52.975, 53.865))
}

# Auto compute all the parameters required for DataShaders
x_range, y_range, plot_width, plot_height = get_plot_params(bboxes["gb"], PLOT_WIDTH)
x_range, y_range = tuple(x_range), tuple(y_range)

# Set options for DataShader.
# TODO: how to make pan and wheel_zoom "on/clicked" by default? (and the rest off/unclicked)
options = dict(tools=['pan', 'wheel_zoom'],
    width=plot_width, height=plot_height, xaxis=None, yaxis=None, bgcolor='black', show_grid=False)

# Our Datashader plot, with additional options
shaded = datashade(points, cmap=cm(Hot,0.1, 0.95), x_range=x_range, y_range=y_range).opts(plot=options)

# Define background maps (tiles) for our Datashader to overlay on later
tiles = {'OpenMap': WMTSTileSource(url='http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png'),
         'ESRI': WMTSTileSource(url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{Y}/{X}.jpg'),
         'Wikipedia': WMTSTileSource(url='https://maps.wikimedia.org/osm-intl/{Z}/{X}/{Y}@2x.png'),
         'Stamen Toner': STAMEN_TONER,
         'STAMEN_TERRAIN': STAMEN_TERRAIN}
tile_geo = gv.WMTS(tiles['ESRI'],crs=crs.GOOGLE_MERCATOR)
tile_map = gv.WMTS(tiles['STAMEN_TERRAIN'],crs=crs.GOOGLE_MERCATOR)

# Our layout will consist of two plots (left and right)
# Left plot: Datashader plot overlaying on a tile map (where we can find street names)
# Right plot: Datashader plot overlaying on a geographical map (where we can see satellite image of landscape)
layout = (tile_map * dynspread(shaded)) + (tile_geo * dynspread(shaded))

# TODO: how to enable hover support for holoview-bokeh-datashader?
# https://github.com/bokeh/datashader/issues/126
# dynamic_hover = datashade(points, width=400, height=400) * \
#     hv.util.Dynamic(aggregate(points, width=10, height=10, streams=[RangeXY]), operation=hv.QuadMesh)
# layoyt = dynamic_hover
# layout = shaded

# Instead of Jupyter's automatic rich display, render the object as a bokeh document (to serve as a web application)
doc = hv.renderer('bokeh').server_doc(layout)
doc.title = 'HoloViews Bokeh App'
# curdoc().add_root(blablabla)
